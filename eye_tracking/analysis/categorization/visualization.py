import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def main(path_to_categorizations):
    """Visualizes the proportion of frames fixated on each object class.

    Keyword arguments: 
    path_to_categorizations -- output of identification.py
    """
	df = pd.read_csv(path_to_categorizations)
	entity_fixation_counts = df.count()

	entities = df.columns[3:]
	counts = entity_fixation_counts.iloc[3:]/len(df)

	sns.barplot(entities, counts)
	plt.xlabel("Entity")
	plt.ylabel("% of frames fixated on")
	plt.title("Entity vs % of frames fixated on")
	plt.show()

if __name__ == '__main__':
	args = sys.argv[1:]
	assert(len(args) >= 1)
	main(args[0])