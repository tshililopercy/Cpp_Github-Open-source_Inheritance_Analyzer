/*******************************Interface Class*************************************/
class A{
    public: 
    virtual void publicpuremethodA1() = 0;
    virtual void publicpuremethodA2() = 0;
    virtual void publicpuremethodA3() = 0;
    private:
    virtual void privatepuremethodA1() = 0;
    virtual void privatepuremethodA2() = 0;
    protected:
};

/***********************************Public Inheritance***************************************/

class B:public A{
    public: 
    virtual void publicpuremethodB1() = 0;
    virtual void publicpuremethodB2() {

    };
    virtual void publicpuremethodB3() {

    };
    private:
    virtual void privatepuremethodB1(){

    };
    virtual void privatepuremethodbB2(){

    };
    protected:
};
/************************************Private Inheritance******************************************/
class C:private A{
    public: 
    virtual void publicpuremethodC1() = 0;
    virtual void publicvirtualmethodC2() {

    };
    virtual void publicvirtualmethodC3() {

    };
    private:
    virtual void privatevirtualmethodC1(){

    };
    virtual void privatevirtualmethodC2(){
        
    };
    protected:
    virtual void protectedvirtualmethodC1(){

    }
};
/***********************************Protected Inheritance**********************************************/
class D:protected A{
    public: 
    virtual void publicpuremethodD1() = 0;
    virtual void publicvirtualmethodD2() {

    };
    virtual void publicvirtualmethodD3() {

    };
    private:
    virtual void privatevirtualmethodD1(){

    };
    virtual void privatevirtualmethodD2(){
        
    };
    protected:
    virtual void protectedvirtualmethodD1(){
        
    }
};