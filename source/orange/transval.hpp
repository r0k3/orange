/*
    This file is part of Orange.

    Orange is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    Orange is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Orange; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

    Authors: Janez Demsar, Blaz Zupan, 1996--2002
    Contact: janez.demsar@fri.uni-lj.si
*/


#ifndef __TRANSVAL_HPP
#define __TRANSVAL_HPP

#include "root.hpp"
#include "orvector.hpp"

WRAPPER(TransformValue);
WRAPPER(Domain);
WRAPPER(ExampleGenerator);

/*  Transforms the value to another value. Transforming can be done 'in place' by replacing the old
    value with a new one (function 'transform'). Alternatively, operator () can be used to get
    the transformed value without replacing the original. Transformations can be chained. */
class TTransformValue : public TOrange {
public:
  __REGISTER_ABSTRACT_CLASS

  PTransformValue subTransform; //P transformation executed prior to this

  TTransformValue(TTransformValue *tr =0);
  TTransformValue(const TTransformValue &old);

  TValue operator()(const TValue &val);

  virtual void transform(TValue &val) =0;
};


class TMapIntValue : public TTransformValue {
public:
  __REGISTER_CLASS

  PIntList mapping; //P a lookup table

  TMapIntValue(PIntList = PIntList());
  TMapIntValue(const TIntList &);

  virtual void transform(TValue &val);
};


class TDiscrete2Continuous : public TTransformValue {
public:
  __REGISTER_CLASS

  int value; //P tvearget value
  bool invert; //P give 1.0 to values not equal to the target
  bool zeroBased; //P if true (default) it gives values 0.0 and 1.0; else -1.0 and 1.0, 0.0 for undefined

  TDiscrete2Continuous(const int =-1, bool invert = false, bool zeroBased = true);
  virtual void transform(TValue &);
};


class TOrdinal2Continuous : public TTransformValue {
public:
  __REGISTER_CLASS

  float factor; //P number of values

  TOrdinal2Continuous(const float & = 1.0);
  virtual void transform(TValue &);
};


class TNormalizeContinuous : public TTransformValue {
public:
  __REGISTER_CLASS

  float average; //P the average value
  float span; //P the value span

  TNormalizeContinuous(const float =0.0, const float =0.0);
  virtual void transform(TValue &);
};

class TEnumVariable;
WRAPPER(Variable)


class TDomainContinuizer : public TOrange {
public:
  __REGISTER_CLASS

  enum { LowestIsBase, FrequentIsBase, NValues, Ignore, ReportError, AsOrdinal, AsNormalizedOrdinal};

  bool zeroBased; //P if true (default) it gives values 0.0 and 1.0; else -1.0 and 1.0, 0.0 for undefined
  bool normalizeContinuous; //P if true (default is false), continuous values are normalized
  int multinomialTreatment; //P 0-lowest value, 1-most frequent (or baseValue), 2-n binary, 3-ignore, 4-error, 5-convert as ordinal, 6-ordinal,normalized
  int classTreatment; //P 3-leave as is unless target is given, 4-error if not continuous nor binary nor target given, 5-convert as ordinal (unless target given)

  TDomainContinuizer();

  PVariable discrete2continuous(TEnumVariable *evar, PVariable wevar, const int &val, bool inv = false) const;
  void discrete2continuous(PVariable var, TVarList &vars, const int &mostFrequent) const;
  PVariable continuous2normalized(PVariable var, const float &avg, const float &span) const;
  PVariable discreteClass2continous(PVariable classVar, const int &targetClass) const;
  PVariable ordinal2continuous(TEnumVariable *evar, PVariable wevar, const float &factor) const;

  PDomain operator()(PDomain, const int &targetClass = -1) const;
  PDomain operator()(PExampleGenerator, const int &weightID, const int &targetClass = -1) const;
};


#endif

