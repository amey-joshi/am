#ifndef _PARTICIPANT_HPP_
#define _PARTICIPANT_HPP_

struct Participant {
    int id;
    int self;
    int seek1;
    int seek2;
    int seek3;

    Participant() {id = self = seek1 = seek2 = seek3 = 0;}
    Participant(int i, int sl, int sk1, int sk2, int sk3) : id(i),
        self(sl), seek1(sk1), seek2(sk2), seek3(sk3) {}
	bool can_pair(const Participant& p) const;
};

bool Participant::can_pair(const Participant& p) const {
	if (this->self == p.seek1 ||
		this->self == p.seek2 ||
		this->self == p.seek3)
		return true;
	else
		return false;
}

#endif
