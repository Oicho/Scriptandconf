/*
**    instruction.hh
**      Created on: 19/3/2013
**      By Gauthier "Oicho" FRIDIERE
**      Contact at: gauthier.fridiere@gmail.com
**    Project name: Corewar/Track
*/

#ifndef INSTRUCTION_HH
# define INSTRUCTION_HH

class Instruction
{
// \const /dec
  public:
    Instruction();
    virtual ~Instruction();

// \members declarations
  private:
    int size_;
    struct pokemon lol_;
// \getter /setter
  public:

// \methods
  public:
    void looping();

};

#endif //! INSTRUCTION_HH