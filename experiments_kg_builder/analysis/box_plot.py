import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('memory.csv')

plt.figure(figsize=(5, 3))
plt.boxplot(data["SDM-RDFizer"], labels=["SDM-RDFizer"])

plt.xlabel('Engine')
plt.ylabel('Memory Usage (MB)')
plt.title('Memory Usage of SDM-RDFizer')
plt.show()

plt.figure(figsize=(5, 3))
plt.boxplot(data["Morph-KGC"], labels=["Morph-KGC"])

plt.xlabel('Engine')
plt.ylabel('Memory Usage (MB)')
plt.title('Memory Usage of Morph-KGC')
plt.show()

plt.figure(figsize=(5, 3))
plt.boxplot(data["RMLMapper"], labels=["RMLMapper"])

plt.xlabel('Engine')
plt.ylabel('Memory Usage (MB)')
plt.title('Memory Usage of RMLMapper')
plt.show()

data = pd.read_csv('results.csv')

plt.figure(figsize=(5, 3))
plt.boxplot(data["SDM-RDFizer"], labels=["SDM-RDFizer"])

plt.xlabel('Engine')
plt.ylabel('Execution Time (sec)')
plt.title('Execution Time of SDM-RDFizer')
plt.show()

plt.figure(figsize=(5, 3))
plt.boxplot(data["Morph-KGC"], labels=["Morph-KGC"])

plt.xlabel('Engine')
plt.ylabel('Execution Time (sec)')
plt.title('Execution Time of Morph-KGC')
plt.show()

plt.figure(figsize=(5, 3))
plt.boxplot(data["RMLMapper"], labels=["RMLMapper"])

plt.xlabel('Engine')
plt.ylabel('Execution Time (sec)')
plt.title('Execution Time of RMLMapper')
plt.show()