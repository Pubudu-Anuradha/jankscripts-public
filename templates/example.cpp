/*

This is just some random code.
Make a file like this with your own template.

*/
#include <iostream>

using namespace std;

typedef long long ll;
typedef long long int lli;

int main()
{
    lli i, j;
    cin >> i >> j;
    for (lli a = 0; a < i; a++)
    {
        for (lli b = 0; b < j; b++)
            cout << a + b << " ";
        cout << endl;
    }
}
