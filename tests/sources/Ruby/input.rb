=begin
    SOURCE:
    http://sandbox.mc.edu/~bennet/ruby/code/units_rb.html
=end

#
# This module provides unit conversion.  The main public name is
# the method ratio, which gives the ratio of two dimensioned expressions, 
# or throws an exception if they do not conform.  The exceptions are also
# public, as are the BaseUnit and RelatedUnit classes, which can be used
# to add conversion information to the module.
#
#   Units.ratio(from, to)
# Will tell you how many to you need to equal from.  From and to are strings
# of the form
#    [ n ] { [ / ] unitname[ ^r ] }+
# Where n is the number of whatever units, defaulting to 1.0.  The unitname
# is a unit or alias created with BaseUnit or RelatedUnit.  Unitnames may
# be separated by spaces or dashes.  Power on the unit defaults to 1.
module Units
public
  # Two new exceptions just for us to pitch.
  class UnitsException < Exception
    # Base class for exceptions invented for this module.
  end

  # A unit expression string couldn't be parsed.
  class UnitParseError < UnitsException
    def initialize(m = "Cannot parse measurement expression")
      super(m)
    end
  end

  # Conversion of units which are not conformable (feet to liters or like 
  # that).
  class UnitConformability < UnitsException
    def initialize(m = "Units not conformable")
      super(m)
    end
  end

  # Abstract base class for units.
  class Unit
    # A list of all the units we know.
    @@units = { }

    # Access to @@units.
    def Unit.exists(n)
      return @@units.has_key?(n)
    end
    def Unit.named(n)
      return @@units[n]
    end

    # If this were Java, I'd define an abstract function isbase() which tells
    # if this object is a BaseUnit or not.
    def initialize(name)
      @name = name
      @@units[name] = self
      @@units[name + 's'] = self
    end
    attr_reader :name
    def alias(*names)
      names.each { |n| @@units[n] = self }
    end
  end

  # This is the base unit class.  There is one base unit for each
  # dimension.  Any unit in the right dimension could be used.
  # The class is just a name and a dimension name.
  class BaseUnit < Unit
    def isbase() 
      return true
    end
    def initialize(name, dname)
      super(name)
      @dimension = dname
    end
    attr_reader :dimension

    # This orders the unit objects arbitrarily, but that is sufficient to
    # sort them and compare lists.
    def <=> (u)
      return object_id <=> u.object_id
    end
  end

private
  # Here are the base units for each dimension.
  BaseUnit.new("meter", "length").alias("m", "metre")
  BaseUnit.new("gram", "mass").alias("g")
  BaseUnit.new("second", "time").alias("s", "sec")

  # A measurement is a number and some numerator and denominator units.
  # The unit lists are kept in lowest terms of base units, though the object
  # may be initialized with any units.
  class Measurement
    def initialize(m, num, denom)
      @mult = m.to_f    # The multiplier.  to_f in case you send an integer.
      @num = num        # The numerator units
      @denom = denom    # The denominator units.
      normalize         # Convert to lowest terms of base units.
    end
    attr_reader :mult, :num, :denom

    # Return the ratio.  Throws conformability.
    def ratio(divby)
      raise UnitConformability.new \
        if @num != divby.num || @denom  != divby.denom
      return @mult / divby.mult
    end

  private
    # Convert to base units only, in lowest terms.
    def normalize
      # Convert the lists to just base units.
      newnum = []
      newdenom = []
      basify(@num, false, newnum, newdenom)
      basify(@denom, true, newdenom, newnum)

      # Now eliminate units which appear in both places.  This depends on
      # an arbitrary ordering of the base units which allows us to compare
      # them in a merge order.
      newnum.sort!
      newdenom.sort!
      @num = [ ]
      @denom = [ ]
      while newnum.length > 0 && newdenom.length > 0
        rel = newnum[0] <=> newdenom[0]
        if rel < 0
          # They are different and the num comes first.  Must be kept.
          @num.push(newnum.shift)
        elsif rel > 0
          # They are different and the denom comes first.  Must be kept.
          @denom.push(newdenom.shift)
        else
          # A match.  Eliminate.
          newnum.shift
          newdenom.shift
        end
      end
      @num.concat(newnum)
      @denom.concat(newdenom)
    end

    # Convert the source list to base, adding the components to ndest and
    # ddest, and multiplying or dividing the measure's number.  The
    # src is a unit list.  These may not be base units, but, if not, the
    # measures they contain will be.
    def basify(src, divide, ndest, ddest)
      for unit in src
        if unit.isbase
          ndest.push(unit)
        else
          @mult = if divide then 
                @mult / unit.related.mult 
          else 
                @mult * unit.related.mult 
          end
          ndest.concat(unit.related.num)
          ddest.concat(unit.related.denom)
        end
      end
    end
  end

  =begin
  # This can be called as (qty, unitex) or just (unitex), where m is
  # taken as 1.0.  Units expression is name[^pwr] [ / name... ]
  # unit names are always alpha.  - is a separator like a space, but not
  # between ^ and pwr.
  def Units.qty(m, s=nil)
    m,s = 1.0,m if s == nil

    # See if there's a number at the front of the expression.
    if s.sub!(/^\s*(\-?(\d+(\.\d*)?|\d*\.\d+))\s*/, '') 
      m *= $1.to_f
    end

    # Collect the stuff needed for the units part.
    num = []
    denom = []

    # What's the next thing?
    puthere = num
    otherone = denom
    while true
      # Strip leading crud, which is spaces or dashes
      s.sub!(/^(\s|\-)*/, '')
      break if s == ''

      # Find the next "thing", which is a unit name or a /.
      s.sub!(%r=^([a-zA-Z]+|/)=, '') or 
        raise UnitParseError.new('Expected unit name or slash at "' + s + '"' )
      thing = $1
      if thing == '/'
        # Swap which list the units go into.
        puthere, otherone = otherone, puthere
      else
        # Unit name.
        Unit.exists(thing) or 
          raise UnitParseError.new('Unknown unit name "' + thing + '"')
        unit = Unit.named(thing)

        # See if there's a ^n
        ct = 1
        top = true
        if s.sub!(/^\s*\^\s*(\-?)(\d+)/, '')
          ct = $2.to_i
          top = false if $1 != ''
        end
        if top
          ct.times { puthere.push(unit) }
        else
          ct.times { otherone.push(unit) }
        end
      end
    end

    return Measurement.new(m, num, denom)
  end
  =end

public
  # Return the ratio.
  def Units.ratio(top, bot)
    return Units.qty(top).ratio(Units.qty(bot))
  end

  # The units that are not basic
  class RelatedUnit < Unit
    def isbase() 
      return false
    end
    def initialize(name, measure)
      super(name)
      measure = Units.qty(measure) if measure.kind_of?(String)
      @related = measure
    end
    attr_reader :related
  end

private
  # Here are all the rest of the units we know about.
  RelatedUnit.new("kilometer", "1000 meter").alias("km")
  RelatedUnit.new("centimeter", "0.01 meter").alias("cm")
  RelatedUnit.new("milimeter", "0.01 meter").alias("mm")
  RelatedUnit.new("inch", "2.54 cm").alias("in")=begin
  RelatedUnit.new("foot", "12 in").alias("ft", "feet")
  RelatedUnit.new("mile", "5280 ft").alias("mi")
  RelatedUnit.new("yard", "3 ft").alias("yd")=end
  RelatedUnit.new("furlong", "660 ft")

  RelatedUnit.new("milliliter", "cm^3").alias("ml", "cc")
  RelatedUnit.new("liter", "1000 ml").alias("l")
  RelatedUnit.new("gallon", "3.785412 liter").alias("gal")
  RelatedUnit.new("quart", "0.25 gal").alias("qt")
  RelatedUnit.new("pint", "0.5 quart").alias("pt")
  RelatedUnit.new("cup", "0.25 quart")

  RelatedUnit.new("acre", "43560 ft^2")
  RelatedUnit.new("hectare", "10000 m^2")

  RelatedUnit.new("minute", "60 sec").alias("min")
  RelatedUnit.new("hour", "60 min").alias("hr")
  RelatedUnit.new("day", "24 hr")
  RelatedUnit.new("week", "7 day").alias("wk")
  RelatedUnit.new("fortnight", "14 day")
  RelatedUnit.new("year", "365.25 day").alias("yr")
  #=begin
  RelatedUnit.new("kilogram", "1000 gram").alias("kg")
  RelatedUnit.new("slug", "14.593903 kg")

  RelatedUnit.new("newton", "kg-m/s^2").alias("N")
  RelatedUnit.new("pound", "4.448222 N").alias("lb")
  #=end

  RelatedUnit.new("joule", "N-m").alias("J")
  RelatedUnit.new("calorie", "0.238846 J").alias("cal")
  RelatedUnit.new("kcal", "1000 cal")
  =begin
  RelatedUnit.new("BTU", "1055.055853 J")

  RelatedUnit.new("watt", "J/s")
  RelatedUnit.new("kilowatt", "1000 watt").alias("kw")
  RelatedUnit.new("horsepower", "746 watt")

  RelatedUnit.new("knot", "1.68781 ft/sec")
  =end
end
