#include<cstdio>
#include<time.h>
#include<stdlib.h>
#include <fstream>
using namespace std;

int main()
{
	srand(time(0));                         //产生随机化种子
    ofstream f_out;
    f_out.open("1.in");
	int n=1000000000;
	
	printf("%d",n);                                      
    char pin[10]={'o','p','q','r','i','y'};
	while(n--)                              //依次产生n个字符串 
	{
		
		printf("\n");
		
		int k=10;
		string res;
        res.clear();
		for(int i=1;i<=k;i++)
		{
			int x,s;                        //x表示这个字符的ascii码 ，s表示这个字符的大小写  
			s=rand()%3;                     //随机使s为1或0，为1就是大写，为0就是小写 
			if(s<=1)                        //如果s=1 
			x=rand()%('z'-'a'+1)+'a';       //将x赋为大写字母的ascii码 
			else{
                int ss=rand()%6;
                if(ss<=1){
                    ss=0;
                }
                if(ss>=3){
                    ss=3;
                }
                x=pin[ss];       //如果s=0，x赋为小写字母的ascii码 
            }
			res+=x;                //将x转换为字符输出 
		}
        f_out<<res<<endl;
		
	}
	return 0;
}