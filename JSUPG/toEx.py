import pandas as pd
##Convert panda Frames to excel sheets
df = pd.read_csv(r"C:\Users\Dell\Documents\University\Unversity2022\Thesis\Hexapod Code\Hexapod---SUPG\JSUPG\SUPG_experiments\BSUPGBOX")
df.to_excel(r"C:\Users\Dell\Documents\University\Unversity2022\Thesis\Hexapod Code\Hexapod---SUPG\JSUPG\SUPG_experiments\BSUPGBOX.xlsx")