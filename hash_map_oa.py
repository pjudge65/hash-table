# Name: Peter Judge
# OSU Email: judgep@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/9/2022
# Description: This program contains methods for the initialization and manipulation of hash maps
#              using Open Address Hashing.


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        If the given key is not contained in the Hash Map - adds the key/value pair to the hash table.

        If the given key is contained in the Hash Map - updates the value at the given key.

        Resizes the table if the function is called and the table load is >= .5
        """

        # resize the table before putting the new key/value pair
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity*2)



        #Hash the index, saves the index for i_initial
        index = self._hash_function(key) % self._capacity
        savedIndex = index
        j = 0


        # updating value if the key is contained in the hash map
        # need two separate algorithms since if containsKey is true, we DON't stop at tombstones
        # if containsKey is False, we stop at the first tombstone and overwrite it
        containsKey = self.contains_key(key)
        if containsKey:
            # iterates through all tombstones and items w/o key
            while self._buckets[index].is_tombstone or self._buckets[index].key != key:
                j = j + 1
                index = (savedIndex + (j * j)) % self._capacity
            # updates value of node containing key
            self._buckets[index].value = value


        # we just want to find the first tombstone or None if containsKey is false
        else:

            # self._is_active => element is non-None and tombston=False
            while self._is_active(self._buckets[index]):
                j = j + 1
                index = (savedIndex + (j*j)) % self._capacity
            # creates a new hash entry object at the first non-active element
            self._buckets[index] = HashEntry(key, value)
            self._size = self._size + 1


    def table_load(self) -> float:
        """
        Returns the hash table load factor (number of elements stored / total number of buckets)
        """

        # calculates and returns the table load
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets contained in the Hash Table
        """

        # initialize count of empty buckets variable
        count = 0

        # counts how many elements are either None or have True tombstones)
        for idx in range(self._buckets.length()):
            if not self._is_active(self._buckets[idx]):
                count = count + 1

        # return count of empties at the end of iteration
        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying hash table, and rehashes all key value pairs into
        the new table.
        """

        # new capacity has to be more than the number of elements
        if new_capacity < self._size:
            return

        # saving a copy of new_array to rehash
        new_array = self._buckets

        # emptying the underlying hash table
        self._buckets = DynamicArray()

        # capacity must be a prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)
        self._capacity = new_capacity

        # allows the array to hold capacity # of spots
        self._size = 0
        for idx in range(self._capacity):
            self._buckets.append(None)

        # iterates through the old array, and rehashes every element into the new array (using put)
        for idx in range(new_array.length()):
            if self._is_active(new_array[idx]):
                self.put(new_array[idx].key, new_array[idx].value)


    def get(self, key: str) -> object:
        """
        If the hash table contains the given key, returns the value associated with that key.

        If the table does not contain the key, returns None
        """

        # if the table doesn't contain the key, we return None
        if self.contains_key(key):

            # hash the key for searching
            index = self._hash_function(key) % self._capacity
            savedIndex = index
            j = 0

            # search the bucket using quadratic probing
            while self._buckets[index].key != key or self._buckets[index].is_tombstone:
                j = j + 1
                index = (savedIndex + (j*j)) % self._capacity

            # returns the desired value
            return self._buckets[index].value


    def contains_key(self, key: str) -> bool:
        """
        Returns a boolean: True if the Hash map contains the given key; False if it does not
        """

        # Empty hash map contains no keys
        if self._size == 0:
            return False

        # hash the index for searching
        index = self._hash_function(key) % self._capacity
        savedIndex = index
        j = 0

        # continue the search until we hit a None
        while self._buckets[index] is not None:

            # true condition only when we find the Key AND it's not a tombstone
            if self._buckets[index].key == key and not self._buckets[index].is_tombstone:
                return True
            j = j + 1
            index = (savedIndex + (j*j)) % self._capacity

        # doesn't contain key if we reached the end of the search
        return False


    def remove(self, key: str) -> None:
        """
        Removes the key/value pair associated with the given key from the hash table if it is found.
        """

        # if the table doesn't contain the key, we're done
        if self.contains_key(key):

            # hash the key for finding the element
            index = self._hash_function(key) % self._capacity
            savedIndex = index
            j = 0

            # use quadratic probing to find the key
            while self._buckets[index].key != key or self._buckets[index].is_tombstone:
                j = j + 1
                index = (savedIndex + (j*j)) % self._capacity

            # set the removed element to be a tombstone and decrement the size
            self._buckets[index].is_tombstone = True
            self._size = self._size - 1






    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing the underlying table capacity
        """

        # sets all buckets to None, and size to 0
        for idx in range(self._capacity):
            self._buckets[idx] = None
        self._size = 0


    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array containing every key/value pair stored in the hash map.
        """

        # initializes output array for appending
        outputArr = DynamicArray()

        # checks every element - if a non-tombstone element, append tuple to output
        for idx in range(self._buckets.length()):
            if self._buckets[idx] is not None and self._buckets[idx].is_tombstone is False:
                outputArr.append((self._buckets[idx].key, self._buckets[idx].value))

        # return the output array
        return outputArr

    def _is_active(self, element: object) -> bool:
        """
        Helper function that receives an element and returns a boolean:
        True if the element is a non-None value, and it's tombstone attribute is False;
        False otherwise.
        """

        # returns whether or not an element is (none or tombstone)
        if element is not None and element.is_tombstone is False:
            return True
        return False


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 0")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(14):
        m.put('str' + str(i), i * 100)
    print(m)

    m.put('str14', 1400)

    print(m)


    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())
