#ifndef _MATCHES_HPP_
#define _MATCHES_HPP_

struct Match {
	int x;
	int y;

	Match() {x = y = 0;}
	Match(int m, int n) : x(m), y(n) {}
	bool same(int m, int n) const {
		return ((x == m) && (y == n)) || ((x == n) && (y == m));
	}
};

#endif

