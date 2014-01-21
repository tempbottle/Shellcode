%define htonq(x) (\
    (((x) & 0x00000000000000ff) << 56) | \
    (((x) & 0x000000000000ff00) << 40) | \
    (((x) & 0x0000000000ff0000) << 24) | \
    (((x) & 0x00000000ff000000) <<  8) | \
    (((x) & 0x000000ff00000000) >>  8) | \
    (((x) & 0x0000ff0000000000) >> 24) | \
    (((x) & 0x00ff000000000000) >> 40) | \
    (((x) & 0xff00000000000000) >> 56))

%define htonl(x) (\
    (((x) & 0x000000ff) << 24) | \
    (((x) & 0x0000ff00) <<  8) | \
    (((x) & 0x00ff0000) >>  8) | \
    (((x) & 0xff000000) >> 24))

%define htons(x) ((((x) & 0xff00) >> 8) | (((x) & 0x00ff) << 8))
%define ip(a,b,c,d) htonl(a << 24 | b << 16 | c << 8 | d) ; ip(127,0,0,1)
