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

class class1: public classA{
    virtual void fxnXA()=0;
};

class class2: public classA, classB{
    virtual void fxnXA()=0;
};

class class3: public classA, classB, classC{
    virtual void fxnXA()=0;
};

class class4: public classA, classC{
    void fxnXB();
};

class class5: public class1{
    void fxnXB1();
};

class class6: public class5, classC{
    void fxnXB1();
};

class class7: public class1{
    virtual void fxnXC()=0;
};
