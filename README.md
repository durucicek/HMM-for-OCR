# HMM-for-OCR
Finding the most likely character sequence via a 1st order Hidden Markov Model, using optical sensor outputs.
This was an homework for the CENG461 Artificial Intelligence course (12.2023).


The objective is to find the most likely character sequence via a 1st order Hidden Markov Model (HMM), using the optical sensor outputs as the observable and the actual letters as hidden states. 
For all states, the only possible values are upper-case English letters. 

In two separate files (data_actual_words.txt and data_ocr_outputs.txt)a list of actual words and their OCR readings are given. 
Using this data, I have computed approximate transition and emittance probabilities. 
Finally, using those probabilities, I have compute the most likely character sequences given OCR observations.
