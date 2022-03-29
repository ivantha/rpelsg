# Realtime Property Evaluation of Large Scale Streaming Graphs

The amount of collected information on data repositories has vastly increased with the advent of the internet. It has become increasingly complex to deal with these massive data streams due to their sheer volume and the throughput of incoming data. Many of these data streams are mapped into graphs, which helps discover some of their properties. However, due to the difficulty in processing massive streaming graphs, they are summarized such that their properties can be approximately evaluated using the summaries. gSketch, TCM, and gMatrix are some of the major streaming graph summarization techniques. Our primary contribution is devising kMatrix, which is much more memory efficient than existing streaming graph summarization techniques. We achieved this by partitioning the allocated memory using a sample of the original graph stream. Through the experiments, we show that kMatrix can achieve a significantly less error for the queries using the same space as that of TCM and gMatrix.

## How to run the experiments

1. Clone the repository by running `git clone https://github.com/ivantha/rpelsg.git`.

2. To go to the project dir, `cd rpelsg/rpelsg-benchmark`.

3. Create a virtual environment following the information [here](https://docs.python.org/3/library/venv.html).

4. Install the requirements using the command, `pip install -r requirements.txt`.

5. Run the test files in the `tests` directory to run each test. 
eg- `python tests/buildtime_test.py`
