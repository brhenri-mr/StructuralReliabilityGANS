import glob
import os 


path = r'C:\Users\Breno HM Rodrigues\Documents\GitHub\StructuralReliabilityGANS\Imagens'

with open('perfils.txt') as nomes:
    for arquivo,nome in zip(glob.glob(r'C:\Users\Breno HM Rodrigues\Documents\GitHub\StructuralReliabilityGANS\Imagens\*.png'),nomes.readlines()):
        nome = nome.replace('\n','')
        os.rename(arquivo,os.path.join(path,f'{nome}.png'))
