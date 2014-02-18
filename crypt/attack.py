import re
import urllib
#from PyCrypto import AES
from hexstr import strxor

"""
The CBC decryption algorthm is 
m[i] = [XOR(IV, D(k, c[0])] + [XOR(c[i-1], D(k, c[i])) for i in range(1, len(c))] 
"""

def website(url=r'http://crypto-class.appspot.com/po?er=f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4',
        mode='CBC',
        get_regex=r'\w*[?][a-zA-Z]+[=]',
        block_size=16):
    rest_getter = re.search(get_regex, url).group()
    print rest_getter
    base_url, c = url.split(rest_getter)
    print base_url, c
    # discard the last block?  don't need to do this, just following example first
    c = c.decode('hex')
    print len(c)
    N = len(c)
    BS = block_size
    m = ['_'] * N
    for j in range(0, N):
        SLB0 = N-(((j/BS)+2)*BS)
        SLBN = N-(((j/BS)+1)*BS)
        SLBi = N-j-BS
        LB0 = SLB0 + BS
        LBN = SLBN + BS
        LBi = SLBi + BS
        print j, SLB0, SLBi, SLBN, LB0, LBi, LBN
        LBhex = c[LB0:LBN].encode('hex')
        SLB_prefix = chr(0) * (SLBi - SLB0)
        SLB_suffix = ''.join(m[(LBi+1):LBN])
        cSLB_suffix = c[SLBi:SLBN]
        pad = chr((j%BS)+1) * ((j%BS)+1)
        print '%r: %r' % (j,  (SLB_prefix + chr(0) + SLB_suffix).encode('hex') + LBhex)
        print '%r: %r' % (j,  (SLB_prefix + pad).encode('hex') + LBhex)
        print '%r: %r' % (j,  (SLB_prefix + strxor(chr(0) + SLB_suffix, pad)).encode('hex') + LBhex)
        for i in range(256):
            g = chr(i)
            SLB = SLB_prefix + strxor(cSLB_suffix, strxor(g + SLB_suffix, pad))
            new_url = base_url + rest_getter + (c[:SLB0] + SLB).encode('hex') + LBhex
            response = urllib.urlopen(new_url)
            print new_url
            if padding_oracle(response):
                break
        m[LBi] = g
        print ''.join(m)
    return ''.join(m)


def padding_oracle(response):
    """Return True if the http response indicates a valid padding block.
    Return False if certainly not a valid pad.
    Return None or a probability 0 < p < 1 if it is uncertain whether the padding is valid
    
    For the coursea app, 404 is returned for an invalid pad,
                         403 for an invalid mac (or url)
                         500 for server fault
                         200 for a valid page load
    """
    return not (padding_oracle.edict.get(response.getcode(), None) == 'pad')
padding_oracle.edict = { 500: 'connection', 404: 'mac', 403: 'pad', 200: 'OK'}


def inject(cypher_text=r'20814804c1767293b99f1d9cab3bc3e7ac1e37bfb15599e5f40eef805488281d',
            plain_text=r'Pay Bob 100$',
            desired_plain_text=r'Pay Bob 500$',
            mode='CBC'):
    "Produce the cyphertext for the requested plain text message without know the key!"
    modified_cypher_text = cypher_text
    return modified_cypher_text