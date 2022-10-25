// A. For Single inheritance

// 1. Private inheritance
// - interface inheritance
// - implementation inheritance
// - type of class
// - visible pure virtual
// - visible virtual 
// - inherited normal functions
// - Overriden functions
// - visible overriden
// - Added Methods 
// - Novel methods

class A{
    public:
    virtual void basepublicpuremethod() = 0;
    virtual void basepublicvirtualmethod(){

    };
    void basepublicnormalmethod(){

    }
    private:
    virtual void baseprivatepuremethod() = 0;
    virtual void baseprivatevirtualmethod(){

    };
    void baseprivatenormalmethod(){

    };
    protected:
    virtual void baseprotectedpuremethod() = 0;
    virtual void baseprotectedvirtualmethod(){

    };
    void baseprotectednormalmethod(){

    };
};

class B: public A{
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

class C{
    public:
    virtual void basepublicpuremethod() = 0;
    virtual void basepublicvirtualmethod(){

    };
    void basepublicnormalmethod(){

    }
    private:
    virtual void baseprivatepuremethod() = 0;
    virtual void baseprivatevirtualmethod(){

    };
    void baseprivatenormalmethod(){

    };
    protected:
    virtual void baseprotectedpuremethod() = 0;
    virtual void baseprotectedvirtualmethod(){

    };
    void baseprotectednormalmethod(){

    };
};

class D: private A{
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

class E: protected A{
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