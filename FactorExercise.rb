#!/usr/bin/ruby ruby

nums = Array[10, 5, 2, 20]

class MyFactor
  # Create the object
  def initialize(number_input  = Array[])
    @numbers2factor = number_input
  end

  #perform factor search
  def get_factors
    @factors = Array.new
    @calc_factors = Array.new

    # check each element against this one
    @numbers2factor.each do |x|
      tf = TermFactor.new(x)
        @factors = Array.new

        @numbers2factor.each do |y|
          if x/y * y == x and x != y
            @factors.push(y)
          end
        end
        tf.set_factors =@factors
      @calc_factors.push(tf)
    end

    @calc_factors
  end

  def show_factors
    cf = get_factors
    @first = true
    print '{'
    cf.each { |t|
      if !@first
        print ', '
      end
      @first = false
      print t.show
    }
    print '}'
  end
end

class TermFactor

  @term
  @factors

  def initialize(t  = 0)
    @term = t
  end

  def set_factors=(f)
    @factors=f
  end

  def show
    print "#{@term}: #{@factors}"
  end
end

f = MyFactor.new(nums)
f.show_factors

# 1. A cache of this computation would use a hash of the input as the key and the calculated output as the value.  Then each term would be calculated and inserted into
# a hashmap style container.  This works fine in memory.  To persist and work from disk the hashed key and streamed result blob would be stored
# in a table.

#    2. The performance of hashing can be as good as O(1).  This could be optimized to eliminate permutations and duplicates in the input.  This would require that the input be normalized
# by sorting and eliminating duplicates.  If this were done then each term would only have one stored result.  The output would have to be assembled
# based on the true input list.  This would add another layer of hashing to retreive each term.

#    3. The cache should be independent of the calculation.  It is simply a lookup for an input mapped to a result.  The optimization of input
# permutation reduction depends on the simple relationship between input terms and output terms.  In the given example there is no difference
# with respect to the cache.