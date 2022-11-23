import pybert as pb

filename = 'DD (res2Dinv format).dat'
tdip = pb.TDIPdata(filename)
tdip.individualInversion()

for i in range(3):
    try:
        ax, cBar = tdip.invertMa(nr=i, show=True, error=0.01, lam=20)
        ax.set_ylim(-33.8, 0)
    except:
        continue

# ax, cBar = tdip.invertMa(nr=5, show=True, error=0.01, lam=100)
# ax.set_ylim(-33.8, 0)