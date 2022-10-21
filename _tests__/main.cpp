class classM1{
    int int_func(){
        int a=0; 
        return a;}

    void void_func(){
        int a1=0;}

    virtual void v_void_func(){
        int a2=0;}
};

class classM2: public classM1{
    void int_funcB(){
       int b=0;}
};
