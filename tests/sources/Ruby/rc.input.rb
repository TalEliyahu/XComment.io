















module Units
public
  
  class UnitsException < Exception
    
  end

  
  class UnitParseError < UnitsException
    def initialize(m = "Cannot parse measurement expression")
      super(m)
    end
  end

  
  
  class UnitConformability < UnitsException
    def initialize(m = "Units not conformable")
      super(m)
    end
  end

  
  class Unit
    
    @@units = { }

    
    def Unit.exists(n)
      return @@units.has_key?(n)
    end
    def Unit.named(n)
      return @@units[n]
    end

    
    
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

  
  
  
  class BaseUnit < Unit
    def isbase() 
      return true
    end
    def initialize(name, dname)
      super(name)
      @dimension = dname
    end
    attr_reader :dimension

    
    
    def <=> (u)
      return object_id <=> u.object_id
    end
  end

private
  
  BaseUnit.new("meter", "length").alias("m", "metre")
  BaseUnit.new("gram", "mass").alias("g")
  BaseUnit.new("second", "time").alias("s", "sec")

  
  
  
  class Measurement
    def initialize(m, num, denom)
      @mult = m.to_f    
      @num = num        
      @denom = denom    
      normalize         
    end
    attr_reader :mult, :num, :denom

    
    def ratio(divby)
      raise UnitConformability.new \
        if @num != divby.num || @denom  != divby.denom
      return @mult / divby.mult
    end

  private
    
    def normalize
      
      newnum = []
      newdenom = []
      basify(@num, false, newnum, newdenom)
      basify(@denom, true, newdenom, newnum)

      
      
      
      newnum.sort!
      newdenom.sort!
      @num = [ ]
      @denom = [ ]
      while newnum.length > 0 && newdenom.length > 0
        rel = newnum[0] <=> newdenom[0]
        if rel < 0
          
          @num.push(newnum.shift)
        elsif rel > 0
          
          @denom.push(newdenom.shift)
        else
          
          newnum.shift
          newdenom.shift
        end
      end
      @num.concat(newnum)
      @denom.concat(newdenom)
    end

    
    
    
    
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

  

public
  
  def Units.ratio(top, bot)
    return Units.qty(top).ratio(Units.qty(bot))
  end

  
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
  
  RelatedUnit.new("kilometer", "1000 meter").alias("km")
  RelatedUnit.new("centimeter", "0.01 meter").alias("cm")
  RelatedUnit.new("milimeter", "0.01 meter").alias("mm")
  RelatedUnit.new("inch", "2.54 cm").alias("in")
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
  
  RelatedUnit.new("kilogram", "1000 gram").alias("kg")
  RelatedUnit.new("slug", "14.593903 kg")

  RelatedUnit.new("newton", "kg-m/s^2").alias("N")
  RelatedUnit.new("pound", "4.448222 N").alias("lb")
  

  RelatedUnit.new("joule", "N-m").alias("J")
  RelatedUnit.new("calorie", "0.238846 J").alias("cal")
  RelatedUnit.new("kcal", "1000 cal")
  
end
