class A{
    public:
    virtual void publicpuremethod1() = 0;
    virtual void publicpuremethod2() = 0;
    private:
    virtual void privatepuremethod1() = 0;
    virtual void privatepuremethod2() = 0;
    protected:
    virtual void protectedpuremethod1() = 0;
    virtual void protectedpuremethod2() = 0;
};

class B{
    public:
    void publicpuremethod1(){

    };
    void publicpuremethod2(){

    };
    private:
    void privatepuremethod1(){

    };
    void privatepuremethod2(){

    };
    protected:
    void protectedpuremethod1(){

    };
    void protectedpuremethod2(){

    };
};