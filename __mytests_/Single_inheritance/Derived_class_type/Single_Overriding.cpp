/**************************INTERFACE CLASS***************************/
class A{
    public: 
    virtual void publicpuremethodA1(int) = 0;
    virtual void publicvirtualmethodA1() = 0;
    private:
    virtual void privatepuremethodA2(int, int) = 0;
    protected:
    virtual void protectedpuremethodA1() = 0;
};
/*************************Pure Virtual Functions Overriding****************************/
class B : public A {
    public:
    virtual void publicpuremethodA1(int){

    }
    private:
    void privatepuremethodA2(int, int){

    }
    protected:
    void protectedpuremethodA1() {

    }
};

class C: public A{
    public:
    virtual void publicpuremethodC1(int){

    }
    private:
    void privatepuremethodC2(int, int){

    }
    protected:
    void protectedpuremethodC1() {

    }
};

/******************************************Virtual Functions Concrete Class********************************************************/
class A2{
    public: 
    virtual void publicpuremethodA2(int){

    };
    virtual void publicvirtualmethodA2(){

    };
    private:
    virtual void privatepuremethodA2(int, int) {

    };
    protected:
    virtual void protectedpuremethodA2() {

    };
};
/**********************************Virtual Functions Overriding****************************************************/

class B2 : public A2 {
    public: 
    virtual void publicpuremethodA2(int){

    };
    virtual void publicvirtualmethodA2(){

    };
    private:
    virtual void privatepuremethodA2(int, int) {

    };
    protected:
    virtual void protectedpuremethodA2() {

    };
};

class C2 : public A2 {
    public: 
    virtual void publicpuremethodB2(int){

    };
    virtual void publicvirtualmethodB2(){

    };
    private:
    virtual void privatepuremethodB2(int, int) {

    };
    protected:
    virtual void protectedpuremethodB2() {

    };
};