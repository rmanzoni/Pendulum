import uproot # https://uproot.readthedocs.io/en/latest/index.html#how-to-install
import pandas

# read data from phyphox
df = pandas.read_csv('accelerations.csv')

# remove last empty column
df = df[df.columns[:-1]]

# mend names for picky ROOT
names = {
    df.columns[0] : 't' ,
    df.columns[1] : 'ax',
    df.columns[2] : 'ay',
    df.columns[3] : 'az',
}

df = df.rename(columns=names)

# save collected dataset in ROOT tree format
fout = uproot.recreate('accelerations.root')
fout['tree'] = df
