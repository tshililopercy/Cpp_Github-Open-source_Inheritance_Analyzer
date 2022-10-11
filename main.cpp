class classA{
    int int_func(){
        int a=0; 
        return a;}

    void void_func(){
        int a1=0;}

    virtual void v_void_func(){
        int a2=0;}
};

class classB: public classA{
    void int_funcB(){
       int b=0;}
};
