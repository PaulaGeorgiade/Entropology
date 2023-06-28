from collections import Counter
import numpy as np

def calc_diversity(sample, q):
    """
    Calculates diversity of the sample (one list)
    
    Parameters
    ----------
    sample : a list items, each item is an observed species
    q : diversity exponent
    
    Returns
    -------
    Diversity of the sample

    """
    r=dict(Counter(sample))
    N = sum(r.values())
    r=np.array([val/N for val in r.values() if val!=0])
    if q==1:
        return np.exp(-sum(r*np.log(r )))
    elif q==0:
        return len(r)
    else:
        return sum(r**q)**(1/(1-q))
    
def calc_gamma_diversity(samples, q, effective= True ):
    """
    Calculates gamma diversity of the community
    
    Parameters
    ----------
    samples : list of lists of items, each item is an observed species
    q : diversity exponent
    effective : if True ( The default is True ), use effective aggregation. If False, use landscape

    Returns
    -------
    Gamma diversity of the sample

    """
    N = sum([len(s) for s in samples])
    sample_set = set()
    for s in samples:
        sample_set.update(s)
    probabilities = {i:0 for i in sample_set}
    if effective:
        for s in samples:
            p = dict(Counter(s))
            for i,val in p.items():
                probabilities[i]+=(val/len(s))
        # print(probabilities)
        probabilities = {key:(val/len(samples))**q for key,val in probabilities.items() if val>0}
    else:
        for s in samples:
            p = dict(Counter(s))
            for i,val in p.items():
                probabilities[i]+=val/N
        probabilities = {key:(val)**q for key,val in probabilities.items() if val>0}
    if q!=1:
        return sum(list(probabilities.values()))**(1/(1-q))
    else:
        return np.exp(-sum(np.array(list(probabilities.values()))*np.log(np.array(list(probabilities.values()) ))))
   
def calc_alpha_diversity(samples, q, effective= True):
    """
    Calculates alpha diversity of the community
    
    Parameters
    ----------
    samples : list of lists of items, each item is an observed species
    q : diversity exponent
    effective : if True ( The default is True ), use effective aggregation. If False, use landscape

    Returns
    -------
    Alpha diversity of the community

    """
    n_samples =len(samples)
    
    N = sum([len(s) for s in samples])
    sample_diversity = np.array([calc_diversity(sample,q)  for sample in samples])
    if effective:
        if q !=1:
            return (1/n_samples*sum((sample_diversity**(1-q))))**(1/(1-q))
        else:
            return np.prod(sample_diversity)**(1/n_samples)
    else:
        weights = [(len(sample)/N)**q for sample in samples]
        weights = np.array(weights)/sum(weights)
        if q !=1:
            return sum(weights*sample_diversity**(1-q))**(1/(1-q))
        else:
            return np.prod(sample_diversity**weights)

  
def calc_beta_diversity(samples, q, effective=True):
    """
    Calculates beta diversity of the community
    
    Parameters
    ----------
    samples : list of lists of items, each item is an observed species
    q : diversity exponent
    effective : if True ( The default is True ), use effective aggregation. If False, use landscape

    Returns
    -------
    Beta diversity of the community

    """
    return calc_gamma_diversity(samples,q,effective)/calc_alpha_diversity(samples,q,effective)
  
def calc_similarity(samples, q, effective = True):
    """
    Calculates similarity of different sites (lists)
    
    Parameters
    ----------
    samples : list of lists of items, each item is an observed species
    q : diversity exponent
    effective : if True ( The default is True ), use effective aggregation. If False, use landscape

    Returns
    -------
    Similarity of the community

    """
    return 2/calc_beta_diversity(samples,q,effective) -1
    