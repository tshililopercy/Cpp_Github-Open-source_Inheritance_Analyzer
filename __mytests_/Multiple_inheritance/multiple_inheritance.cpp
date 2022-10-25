class A{
    public:
    virtual void basepublicpuremethodA() = 0;
    virtual void basepublicvirtualmethodA(){

    };
    void basepublicnormalmethodA(){

    }
    private:
    virtual void baseprivatepuremethodA() = 0;
    virtual void baseprivatevirtualmethodA(){

    };
    void baseprivatenormalmethodA(){

    };
    protected:
    virtual void baseprotectedpuremethodA() = 0;
    virtual void baseprotectedvirtualmethodA(){

    };
    void baseprotectednormalmethodA(){

    };
};

class B{
    public:
    virtual void basepublicpuremethodB() = 0;
    virtual void basepublicvirtualmethodB(){

    };
    void basepublicnormalmethodB(){

    }
    private:
    virtual void baseprivatepuremethodB() = 0;
    virtual void baseprivatevirtualmethodB(){

    };
    void baseprivatenormalmethodB(){

    };
    protected:
    virtual void baseprotectedpuremethodB() = 0;
    virtual void baseprotectedvirtualmethodB(){

    };
    void baseprotectednormalmethodB(){

    };
};
/*****************************Public, Public Multiple Inheritance*********************************/
class C:public A, public B{
    public:
    virtual void derivedpublicpuremethod() = 0;
    virtual void derivedpublicvirtualmethod(){

    };
    void derivedpublicnormalmethod(){

    }
    private:
    virtual void derivedprivatepuremethod() = 0;
    virtual void derivedprivatevirtualmethod(){

    };
    void derivedprivatenormalmethod(){

    };
    protected:
    virtual void derivedprotectedpuremethod() = 0;
    virtual void derivedprotectedvirtualmethod(){

    };
    void derivedprotectednormalmethod(){

    };
};

/*****************************Public, Private Multiple inheritance*********************************/
class D:public A, private B{
    public:
    virtual void derivedpublicpuremethod() = 0;
    virtual void derivedpublicvirtualmethod(){

    };
    void derivedpublicnormalmethod(){

    }
    private:
    virtual void derivedprivatepuremethod() = 0;
    virtual void derivedprivatevirtualmethod(){

    };
    void derivedprivatenormalmethod(){

    };
    protected:
    virtual void derivedprotectedpuremethod() = 0;
    virtual void derivedprotectedvirtualmethod(){

    };
    void derivedprotectednormalmethod(){

    };
};
/*******************************Public, Protected Multiple inheritance********************************************/
class E:public A, protected B{
    public:
    virtual void derivedpublicpuremethod() = 0;
    virtual void derivedpublicvirtualmethod(){

    };
    void derivedpublicnormalmethod(){

    }
    private:
    virtual void derivedprivatepuremethod() = 0;
    virtual void derivedprivatevirtualmethod(){

    };
    void derivedprivatenormalmethod(){

    };
    protected:
    virtual void derivedprotectedpuremethod() = 0;
    virtual void derivedprotectedvirtualmethod(){

    };
    void derivedprotectednormalmethod(){

    };
};