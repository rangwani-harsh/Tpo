#include<bits/stdc++.h>/* In the name of God we code */
using namespace std;
#define debug(a)    			cerr<<#a<<": ";for(auto i:a)cerr<<i<<" ";cerr<<'\n';
#define show1(a,n) 			cout<<endl;for(int i=0;i<n;i++){cout<<a[i]<<" ";}
#define show2(a,n,m) 			cout<<endl;for(int i=0;i<n;i++){for(int j=0;j<m;j++){cout<<a[i][j]<<" ";}cout<<endl;}

#define trace1(x)                cerr << #x << ": " << x << endl;
#define trace2(x, y)             cerr << #x << ": " << x << " | " << #y << ": " << y << endl;
#define trace3(x, y, z)          cerr << #x << ": " << x << " | " << #y << ": " << y << " | " << #z << ": " << z << endl;
#define trace4(a, b, c, d)       cerr << #a << ": " << a << " | " << #b << ": " << b << " | " << #c << ": " << c << " | " << #d << ": " << d << endl;
#define trace5(a, b, c, d, e)    cerr << #a << ": " << a << " | " << #b << ": " << b << " | " << #c << ": " << c << " | " << #d << ": " << d << " | " << #e << ": " << e << endl;
#define trace6(a, b, c, d, e, f) cerr << #a << ": " << a << " | " << #b << ": " << b << " | " << #c << ": " << c << " | " << #d << ": " << d << " | " << #e << ": " << e << " | " << #f << ": " << f << endl;

#define pb(i) 				push_back(i)
#define mp(i,j) 			make_pair(i,j)
#define mod 				1000000007
#define F           			first
#define S           			second
#define endl        			'\n'
#define ll 				long long
#define pii           pair <int,int>
#define N 1000010
int arr[N];
int main(int argc, char const *argv[])
{
	int n,p;
	cin>>n>>p;
	for(int i=0;i<n;i++){
		cin>>arr[i];
	}
	sort(arr,arr+n);
	int minx = INT_MAX;
	for(int i=0;i<n;i++){
		minx = min(minx,arr[i] - p*(i+1));


	}
	cout<<minx<<endl;
	return 0;
}