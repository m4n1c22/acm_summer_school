size_t compress_line(cacheline* line) {

  //cerr << line->float32[4].b.exp << endl;
  int i, nzeros=0, nibbles_zeros=0;
  for(i=0;i<64;i++) {
     if(line->byte[i]==0) {
        nzeros+=2;
     }
     else {
        if(nzeros!=0) {

        }
     }
  }
  if(nzeros>1) {
     nibbles_zeros+=nzeros;
  }
  return nibbles_zeros/2;
}
