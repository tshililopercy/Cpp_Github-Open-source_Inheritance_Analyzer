/*****************************Interface Class***********************************/
class A {
    public:
    virtual void publicpuremethodA1() = 0;
    private:
    virtual void privatepuremethodA1() = 0;
    protected:
    virtual void protectedpuremethodA1() = 0;
};
/*****************************Overring all Base Class pure virtual functions***********************************/
class B: public A{
    public:
    virtual void publicpuremethodA1(){

    }
    private:
    virtual void privatepuremethodA1(){

    };
    protected:
    virtual void protectedpuremethodA1(){

    };
};
/*******************************************Override Some Base class Pure Virtual functions*****************************************************************/
class C: public A{
    public:
    virtual void publicpuremethodA1(){

    }
    private:
    virtual void privatepuremethodA1(){

    };
    protected:
};
/********************Doesn't override Base class Pure Virtual functions And Add Pure Virtual functions************************************************/
class D: public A{
    public:
    virtual void publicpuremethodD1() = 0;
    private:
    virtual void privatepuremethodD1() = 0; 
    protected:
};
/*********************Override All Base Base class and Add pure virtual functions*******************************************************/
class E: public A{
        public:
    virtual void publicpuremethodA1(){

    }
    virtual void publicpuremethodE1() = 0;
    private:
    virtual void privatepuremethodA1(){

    };
    protected:
    virtual void protectedpuremethodA1(){

    };
};