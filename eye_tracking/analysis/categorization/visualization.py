import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def main():
	df = pd.read_csv("targets.csv")
	entity_fixation_counts = df.count()

	entities = df.columns[3:]
	counts = entity_fixation_counts.iloc[3:]/len(df)

	sns.barplot(entities, counts)
	plt.xlabel("Entity")
	plt.ylabel("% of frames fixated on")
	plt.title("Entity vs % of frames fixated on")
	plt.show()

if __name__ == '__main__':
    main()