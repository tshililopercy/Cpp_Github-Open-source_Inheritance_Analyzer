class classA{
    virtual void pure_func()=0;
    virtual void pureA_func()=0;
};

class classB{
    void void_func(){int a=0;}
    virtual void v_void_func(){int a1=0;}
};

class classC{
    virtual void pure_funcC()=0;
    void void_funcC(){int c=0;}
};

class classXA: public classA{
    virtual void fxnXA()=0;
};

class classXB: public classB{
    virtual void fxnXB()=0;
};

class classXB1: public classB{
    void fxnXB1();
};

class classXC: public classC{
    virtual void fxnXC()=0;
};
