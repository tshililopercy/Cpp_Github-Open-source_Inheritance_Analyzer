/*******************************Concrete Class*************************************/
class A{
    public: 
    void publicpuremethodA1(int, int) {

    };
    void publicpuremethodA2(int) {

    };
    void publicpuremethodA3(int, float) {
        
    };
    private:
    void privatepuremethodA1(){

    };
    virtual void privatepuremethodA2(){
        
    };
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