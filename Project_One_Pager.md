5/19/16

**Research Problem**

For my project, I will perform a quantitative analysis of literary style. Style is a commonly recognized aspect of literature, but is often defined vaguely as something like “the way an author writes.” The goal of this project is to turn that abstract concept into a specific, concrete set of characteristics that distinguish a given author’s work. The output of the project will be a machine learning model that, given a sample of text, returns the probability that the text was written by each of the authors that the model is familiar with.

**Dataset**

For this analysis, I have collected electronic copies of works from four contemporaneous authors: Ernest Hemingway, F. Scott Fitzgerald, John Steinbeck, and William Faulkner. I will include three books from each author in the dataset.

Each of these books was converted from an e-book file (.epub or .mobi) to a text file using the free Calibre e-book manager tool. Considerable pre-processing will be required of each text before any analysis can be conducted in order to establish a common format, as the encoding of the text, the delineation of chapters, the inclusion and formatting of page numbers, etc. varies between each work.

**Feature Definition**

Before conducting any analysis, I will divide each text into uniformly sized blocks that will serve as the level of observation for analysis. This approach allows a more granular view into each book than using the entire text, providing more data points for inference and letting me compare the variance of a feature within a single work to the variance of that feature across the author’s works as a whole. The block size will be easy to adjust, so I will able to construct multiples models based on different block sizes and observe how the choice of block size affects performance.

With this block structure in mind, the features that I will use for prediction can be described as occurring at either the word level, the sentence level, or the block level. Word-level features may include: the length of the word, the number of syllables in the word, the etymology of the word, and the year in which the word was most commonly used. Sentence-level features may include: the number of words in the sentence, the number of clauses in the sentence, the structure of the sentence, and the sentiment of the sentence.

For features observed at either of these two levels, some aggregation to the block level will be necessary, which presents opportunities for testing different interpretations (e.g. which is a better predictor: the avg. length of sentences in a block or the percentage of sentences in a block with more than 30 words?).

Block-level features may include the use of punctuation in the block, the percentage of the block that is dialogue, the gender ratio of names mentioned in the block, the lexical diversity of the block, the frequency of so-called “function words” within the block (see attached paper by Peng and Hengartner for more information on function words), and the location of real-world places mentioned in the block.

**Methodology**

To conduct the analysis, I will likely use a naïve Bayes classifier to predict the probability that a given snippet of text was written by each of the four authors included in the training set. Ideally the text used for testing should not need to be a block of the same size that was used to train the model, so it will be important to normalize all of the features when defining them.

The Peng and Hengartner paper uses PCA on the frequency of “function words” as a pre-processing step to prediction, so I may also recreate their methodology on my dataset if time permits.

There are also a number of possibilities for interesting visualizations of the features as part of the exploratory data analysis phase of this project, even for dimensions that might not make it into the final model. These might include a heatmap of the locations mentioned in the texts by author, what particular words most identify an author (e.g. how often does Hemingway talk about booze and cafes?), or the average Scrabble score of the words an author uses, among others.

**Current Progress**

So far, I have collected all of the books to be used in the analysis, converted them all to text files, and performed the necessary cleaning on one book (The Sun Also Rises by Hemingway) to start measuring its features. I have been using that cleaned text to begin writing the functions that will be used to break all of the texts into blocks and define the features. I’m currently most of the way through defining the functions for the word-level features, after which I’ll move on to the sentence-level and block-level features.

Once those functions have all been built, I will finish munging each of the individual text files for the other books so that I can run them through the feature-defining functions, perform some exploratory data analysis, and begin actual modeling. 
