import pandas as pd
import pystra as ra


#coletar dados do excel com os valores do perfil 


def dados(path:str)->pd.DataFrame:
    return pd.read_excel(path,names=['bitola','h','bf','tw','tf'])

#função d estado limite
def g(fy:int,h:float,tw:float,bf:float,tf:float):
    '''
    Retorna a função de estado limite
    fy: Resistência caracteristica de escoamento
    h: altura da alma
    tw: espessura da alma
    bf: comprimento da mesa/flange 
    tf: espessura da mesa/flange
    q: carga distribuida 
    L: comprimento do vão
    '''

    inercia = h**3*(tw)/12+2*(bf*tf*(h/2+tf/2)**2+bf*tf**3/12)

    limit_state = ra.LimitState(lambda q,L: fy- (q*(L**2)/8)*(h/2+tf)/(inercia))

    return limit_state


def preprocessamento(bd:pd.DataFrame,drop=None,multiplo = 4) ->pd.DataFrame:
    '''
    Pre processamento dos dados
    bd: Banco de Dados
    multiplo: quantidade de elementos repetidos no enchimento dos dos
    '''

    if drop != None:
        bd = bd.drop(columns=drop)


    bd = bd.sort_values(['prob'],ascending=False)
    saida = pd.DataFrame()

    prob = bd['prob'].drop_duplicates()

    for i in prob:

        fil = bd[bd['prob']<=i]

        fil['prob'] = fil['prob'].apply(lambda x:i)
        for _ in range(multiplo):
            saida = pd.concat([saida,fil],ignore_index=True)


    return saida


dados('BancoDados.xlsx')

bd = dados('BancoDados.xlsx')

prob= []



for i in range(bd['bitola'].shape[0]):
    limite = g(35,bd['h'][i],bd['tw'][i],bd['bf'][i],bd['tf'][i])


    stochastic_model = ra.StochasticModel()

    stochastic_model.addVariable(ra.Lognormal("q", 5, 10))
    stochastic_model.addVariable(ra.Constant("L", 300))

    options = ra.AnalysisOptions()
    options.setPrintOutput(False)

    # initialize analysis obejct
    Analysis = ra.Form(
        analysis_options=options,
        stochastic_model=stochastic_model,
        limit_state=limite,
    )

    ''' Analysis.run() # run analysis
    failure = Analysis.getFailure()
    Analysis.showDetailedOutput()'''

    
    # initialize analysis obejct
    cmc = ra.CrudeMonteCarlo(
        analysis_options=options,
        stochastic_model=stochastic_model,
        limit_state=limite,
    )

    cmc.run()
    failure = cmc.getFailure()

    prob.append(round(failure,2))

bd['prob'] = prob


saida = preprocessamento(bd,drop=['h','bf','tw','tf'])

print(saida[saida['prob']==0.74])

saida.to_excel('saida.xlsx')
#bd.to_excel('saida.xlsx')

#*******