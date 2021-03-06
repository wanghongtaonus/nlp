from code_to_comment.model import Transformer
import tensorflow as tf
import json
import numpy as np
import sys,os
print(sys.path[0])
for pth in sys.path:
    print(pth)
# sys.path.append(os.path.split(sys.path[0])[0])
print(os.path.split(sys.path[0]))
# hyper-params
num_layers = 4
d_model = 128
dff = 512
num_heads = 8
EPOCHS = 100
encoder_maxlen = 400
decoder_maxlen = 75
code_path = './dataset1/camel_code.txt'
comment_path = './dataset1/comment.txt'
logdir = './runs/test'
here = os.path.dirname(os.path.abspath(__file__))
code_tokenizer_path = os.path.join(here, 'code_tokenizer.json')
comment_tokenizer_path=os.path.join(here,'comment_tokenizer.json')
with open(code_tokenizer_path, 'r') as f:
    code_tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(json.load(f))
with open(comment_tokenizer_path, 'r') as f:
    comment_tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(json.load(f))

encoder_vocab_size = len(code_tokenizer.word_index) + 1
decoder_vocab_size = len(comment_tokenizer.word_index) + 1

transformer = Transformer(
    num_layers, 
    d_model, 
    num_heads, 
    dff,
    encoder_vocab_size, 
    decoder_vocab_size, 
    pe_input=encoder_vocab_size, 
    pe_target=decoder_vocab_size,
)

def create_padding_mask(seq):
    seq = tf.cast(tf.math.equal(seq, 0), tf.float32)
    return seq[:, tf.newaxis, tf.newaxis, :]

def create_look_ahead_mask(size):
    mask = 1 - tf.linalg.band_part(tf.ones((size, size)), -1, 0)
    return mask

def create_masks(inp, tar):
    enc_padding_mask = create_padding_mask(inp)
    dec_padding_mask = create_padding_mask(inp)

    look_ahead_mask = create_look_ahead_mask(tf.shape(tar)[1])
    dec_target_padding_mask = create_padding_mask(tar)
    combined_mask = tf.maximum(dec_target_padding_mask, look_ahead_mask)
  
    return enc_padding_mask, combined_mask, dec_padding_mask



def evaluate(input_document):
    input_document = code_tokenizer.texts_to_sequences([input_document])
    input_document = tf.keras.preprocessing.sequence.pad_sequences(input_document, maxlen=encoder_maxlen, padding='post', truncating='post')

    encoder_input = tf.expand_dims(input_document[0], 0)

    decoder_input = [comment_tokenizer.word_index["<go>"]]
    output = tf.expand_dims(decoder_input, 0)
    
    for i in range(decoder_maxlen):
        enc_padding_mask, combined_mask, dec_padding_mask = create_masks(encoder_input, output)

        predictions, attention_weights = transformer(
            encoder_input, 
            output,
            False,
            enc_padding_mask,
            combined_mask,
            dec_padding_mask
        )

        predictions = predictions[: ,-1:, :]
        predicted_id = tf.cast(tf.argmax(predictions, axis=-1), tf.int32)

        if predicted_id == comment_tokenizer.word_index["<stop>"]:
            return tf.squeeze(output, axis=0), attention_weights

        output = tf.concat([output, predicted_id], axis=-1)

    return tf.squeeze(output, axis=0), attention_weights

def summarize(input_document):
    # not considering attention weights for now, can be used to plot attention heatmaps in the future
    summarized = evaluate(input_document=input_document)[0].numpy()
    summarized = np.expand_dims(summarized[1:], 0)  # not printing <go> token
    return comment_tokenizer.sequences_to_texts(summarized)[0]  # since there is just one translated document

summarize(' ')
transformer.load_weights(here + '/model_epoch5.h5')



def code_to_com(code):
	return summarize(code)



print(code_to_com('public synchronized void info ( string msg ) { log record record = new log record ( level . info , msg ) ; log ( record ) ; }'))