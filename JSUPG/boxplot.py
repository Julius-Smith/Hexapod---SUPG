import csv
import matplotlib.pyplot as plt


##open CSUPG box and create trial arrays
fileC = open(r'C:\Users\Dell\Documents\University\Unversity2022\Thesis\Hexapod Code\Hexapod---SUPG\JSUPG\SUPG_experiments\ECSUPGBOXnormalised.csv')

CTrial1 = []
CTrial2 = []
CTrial3 = []
CTrial4 = []
CTrial5 = []

Clines = csv.reader(fileC, delimiter = ',')
counter = 0

next(Clines)
for row in Clines:
    if row[1]:
        CTrial1.append(float(row[1]))
    if row[2]:
        CTrial2.append(float(row[2]))
    if row[3]:
        CTrial3.append(float(row[3]))
    if row[4]:
        CTrial4.append(float(row[4]))
    if row[5]:
        CTrial5.append(float(row[5]))

# #open BSUPG box
fileB= open(r'C:\Users\Dell\Documents\University\Unversity2022\Thesis\Hexapod Code\Hexapod---SUPG\JSUPG\SUPG_experiments\EBSUPGBOXnormalised.csv')

BTrial1 = []
BTrial2 = []
BTrial3 = []
BTrial4 = []
BTrial5 = []

Blines = csv.reader(fileB, delimiter = ',')

next(Blines)
for row in Blines:
    if row[1]:
        BTrial1.append(float(row[1]))
    if row[2]:
        BTrial2.append(float(row[2]))
    if row[3]:
        BTrial3.append(float(row[3]))
    if row[4]:
        BTrial4.append(float(row[4]))
    if row[5]:
        BTrial5.append(float(row[5]))




dataTest = [CTrial1, CTrial2, CTrial3, CTrial4, CTrial5]
dataB = [BTrial1, BTrial2, BTrial3, BTrial4, BTrial5]

data = [CTrial1, BTrial1, CTrial2, BTrial2, CTrial3, BTrial3, CTrial4, BTrial4, CTrial5, BTrial5]
fig = plt.figure(figsize =(10, 7))

ax = fig.add_subplot(111)



bp = ax.boxplot(data, patch_artist = True,
                notch ='True')

# bp1 = ax.boxplot(dataTest, patch_artist = True,
#                 notch ='True')

# ##make a bp2 for the bSUPG data
# bp2 = ax.boxplot(dataB, patch_artist = True,
#                 notch ='True')

colors = ['darkkhaki', 'royalblue']
numboxs = 10
counter = 0

for patch in bp['boxes']:
    patch.set_facecolor(colors[counter%2])
    counter+=1

for whisker in bp['whiskers']:
    whisker.set(color ='#8B008B',
                linewidth = 1.5,
                linestyle =":")

# # for whisker in bp2['whiskers']:
#     whisker.set(color ='#8B008B',
#                 linewidth = 1.5,
#                 linestyle =":")
                
# for patch in bp1['boxes']:
#     patch.set_facecolor('b')

# for patch in bp2['boxes']:
#     patch.set_facecolor('g')

for median in bp['medians']:
    median.set(color ='red',
               linewidth = 3)

# for median in bp2['medians']:
#     median.set(color ='red',
#                linewidth = 3)

for flier in bp['fliers']:
    flier.set(marker ='D',
              color ='#e7298a',
              alpha = 0.5)

# for flier in bp2['fliers']:
#     flier.set(marker ='D',
#               color ='#e7298a',
#               alpha = 0.5)

# plt.set_xticklabels(['Trial1', 'Trial2',
#                     'Trial3', 'Trial4', 'Trial5'])


#legend
ax.legend([bp["boxes"][0], bp["boxes"][1]], ["CSUPG", "BSUPG"], loc='upper right')
#ax.legend([bp1["boxes"][0]], ["CSUPG"], loc='upper right')
plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ['S0', 'S0',
                    'S1', 'S1', 'S2', 'S2', 'S3', 'S3', 'S4', 'S4'])
plt.title("SUPG Performance")
plt.ylabel('Task Performance')

plt.savefig(r'C:\Users\Dell\Documents\University\Unversity2022\Thesis\Hexapod Code\Hexapod---SUPG\JSUPG\SUPG_experiments\SUPGBoxPlot.png')
plt.show()