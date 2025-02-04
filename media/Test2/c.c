#include <stdio.h>
int sub(int n)
{
    double a,b,c,d,x1,x2,x3,x4,v1,v2,v3,v;
    a=n%10;
    b=((n/10))%10;
    c=((n/100))%10;
    d=(n/1000);
    if((a>b)&& (a>c) && (a>d))
    {x1=a;
    if((b>c) && (b>d))
    {x2=b;
    if(c>d)
    {x3=c;
    x4=d;}
    else
    {x3=d;
    x4=c;}}
    else if((c>b) && (c>d))
    {x2=c;
    if(b>d)
    {x3=b;
    x4=d;}
    else
    {x3=d;
    x4=b;}}
    else 
    {x2=d;
    if(b>c)
    {x3=b;
    x4=c;}
    else
    {x3=c;
    x4=b;}}}

    else if((b>a)&& (b>c) && (b>d))
    {x1=b;
    if((a>c) && (a>d))
    {x2=a;
    if(c>d)
    {x3=c;
    x4=d;}
    else
    {x3=d;
    x4=c;}}
    else if((c>a) && (c>d))
    {x2=c;
    if (a>d)    
    {x3=a;
    x4=d;}
    else
    {x3=d;
    x4=a;}}
    else 
    {x2=d;
    if(a>c)
    {x3=a;
    x4=c;}
    else
    {x3=c;
    x4=a;}}}

    else if((c>a)&& (c>b) && (c>d))
    {x1=c;
    if((a>b) && (a>d))
    {x2=a;
    if(b>d)
    {x3=b;
    x4=d;}
    else
    {x3=d;
    x4=b;}}
    else if((b>a) && (b>d))
    {x2=b;
    if(a>d)
    {x3=a;
    x4=d;}
    else
    {x3=d;
    x4=a;}}
    else 
    {x2=d;
    if(a>b)
    {x3=a;
    x4=b;}
    else
    {x3=b;
    x4=a;}}}

    else
    {x1=d;
    if((a>b) && (a>c))
    {x2=a;
    if(b>c)
    {x3=b;
    x4=c;}
    else
    {x3=d;
    x4=b;}}
    else if((b>a) && (b>c))
    {x2=b;
    if(a>c)
    {x3=a;
    x4=c;}
    else
    {x3=c;
    x4=a;}}
    else 
    {x2=c;
    if(a>b)
    {x3=a;
    x4=b;}
    else
    {x3=b;
    x4=a;}}}

    v1=(x4*1000)+(x3*100)+(x2*10)+x1;
    v2=(x1*1000)+(x2*100)+(x3*10)+x4;
    v=v1-v2;
    return v;
}

int main()
{
    double n,a=0,n1;
    int v,x=1;
    printf("enter the 4 digit number:");
    scanf("%lf",&n);
    n1=n;
    while (x==1)
    {v=sub(n1);
    a=a+1;
    if (v==n)
    break;
    n1=v; }
    printf("the no of times its subtracted and exicuted=%lf",a);
    return 0;
}
