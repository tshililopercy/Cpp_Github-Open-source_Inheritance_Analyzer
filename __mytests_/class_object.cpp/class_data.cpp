class A{
    public:
    virtual void publicpuremethodA() = 0;
    virtual void publicvirtualmethodA(int ) {

    };
    void int privatenormalmethodA(){

    };
    private:
    virtual void privatepuremethodA() = 0;
    virtual void privatevirtualmethodA(){

    };
    void int privatenormalmethodA(){

    }
    protected:
    virtual void protectedpuremethodA() = 0;
    virtual void protectedvirtualmethodA(){

    };
    void int protectednormalmethodA(){

    }
};

class B: public A{
    public:
    virtual void publicpuremethodB() = 0;
    virtual void publicvirtualmethodB(int ) {

    };
    void int privatenormalmethodB(){

    };
    private:
    virtual void privatepuremethodB() = 0;
    virtual void privatevirtualmethodB(){

    };
    void int privatenormalmethodB(){

    }
    protected:
    virtual void protectedpuremethodB() = 0;
    virtual void protectedvirtualmethodB(){

    };
    void int protectednormalmethodB(){

    }
};

class C: private A{
    public:
    virtual void publicpuremethodB() = 0;
    virtual void publicvirtualmethodB(int ) {

    };
    void int privatenormalmethodB(){

    };
    private:
    virtual void privatepuremethodB() = 0;
    virtual void privatevirtualmethodB(){

    };
    void int privatenormalmethodB(){

    }
    protected:
    virtual void protectedpuremethodB() = 0;
    virtual void protectedvirtualmethodB(){

    };
    void int protectednormalmethodB(){

    }
};

class G: protected A{
    public:
    virtual void publicpuremethodB() = 0;
    virtual void publicvirtualmethodB(int ) {

    };
    void int privatenormalmethodB(){

    };
    private:
    virtual void privatepuremethodB() = 0;
    virtual void privatevirtualmethodB(){

    };
    void int privatenormalmethodB(){

    }
    protected:
    virtual void protectedpuremethodB() = 0;
    virtual void protectedvirtualmethodB(){

    };
    void int protectednormalmethodB(){

    }
}

class D: public C, public B{
    public:
    virtual void publicpuremethodB() = 0;
    virtual void publicvirtualmethodB(int ) {

    };
    void int privatenormalmethodB(){

    };
    private:
    virtual void privatepuremethodB() = 0;
    virtual void privatevirtualmethodB(){

    };
    void int privatenormalmethodB(){

    }
    protected:
    virtual void protectedpuremethodB() = 0;
    virtual void protectedvirtualmethodB(){

    };
    void int protectednormalmethodB(){

    }
};

class E: private B, private A{
    public:
    virtual void publicpuremethodB() = 0;
    virtual void publicvirtualmethodB(int ) {

    };
    void int privatenormalmethodB(){

    };
    private:
    virtual void privatepuremethodB() = 0;
    virtual void privatevirtualmethodB(){

    };
    void int privatenormalmethodB(){

    }
    protected:
    virtual void protectedpuremethodB() = 0;
    virtual void protectedvirtualmethodB(){

    };
    void int protectednormalmethodB(){

    }
};
class F: private C, public D{
    public:
    virtual void publicpuremethodB() = 0;
    virtual void publicvirtualmethodB(int ) {

    };
    void int privatenormalmethodB(){

    };
    private:
    virtual void privatepuremethodB() = 0;
    virtual void privatevirtualmethodB(){

    };
    void int privatenormalmethodB(){

    }
    protected:
    virtual void protectedpuremethodB() = 0;
    virtual void protectedvirtualmethodB(){

    };
    void int protectednormalmethodB(){

    }
};

