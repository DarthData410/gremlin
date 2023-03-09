
import pseudoactr as pse

if __name__=="__main__":
    psa = pse.PseudoActor("192.168.56.1",41011)
    psa.reg()
    print(psa.paCliRegACKMsg().return_result())
    print(psa.paCliRegACK())
    print(psa.paCliRegACK().PseudoActor)
    print(psa.paCliRegACK().Registered)

    
    #reg = pse.register("192.168.56.1",41011,pse.lib.genuid(),pse.lib.getnow())
    #reg.execute()