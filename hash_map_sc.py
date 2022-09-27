# Name: Peter Judge
# OSU Email: judgep@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/9/22
# Description: This program contains methods for the initialization and manipulation of hash maps
#              using chained addressing.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        If the given key is not contained in the Hash Map - adds the key/value pair.

        If the given key is contained in the Hash Map - updates the value at the given key.
        """

        # Hashing the index
        index = self._hash_function(key) % self._capacity

        # Iterates through the given bucket, searching for given key
        for node in self._buckets[index]:

            # if key is found, update value at that node and exit function
            if node.key == key:
                node.value = value
                return

        # if key is not found, add key/value pair in new node at front of bucket
        self._buckets[index].insert(key, value)
        self._size = self._size + 1



    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets contained in the Hash Table
        """

        # used to count number of empty buckets
        count = 0

        # iterates through every bucket, counting how many are empty
        for index in range(self._capacity):
            if self._buckets[index]._head is None:
                count = count+1

        # returns number of empty buckets
        return count

    def table_load(self) -> float:
        """
        Returns the hash table load factor (number of elements stored / total number of buckets)
        """

        # calculates and returns the table load
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears the contents of the hash map without altering the underlying capacity.
        """

        # iterates through every bucket and clears each linked list (by clearing the head pointer)
        for index in range(self._capacity):
            self._buckets[index]._head = None

        # new number of elements stored goes to zero
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying hash table, and rehashes all key value pairs into
        the new table.
        """

        # function does nothing if we ask for a capacity <1
        if new_capacity < 1:
            return

        # make sure the new capacity is prime
        if self._is_prime(new_capacity):
            self._capacity = new_capacity
        else:
            self._capacity = self._next_prime(new_capacity)

        # saves the old buckets array to iterate through
        old_array = self._buckets

        # creates an intermediate array to serve as the new buckets ( with new capacity)
        new_array = DynamicArray()
        for idx in range(self._capacity):
            new_array.append(LinkedList())
        self._buckets = new_array
        self._size = 0


        # need to iterate through every array element AND each node in Linked LIst
        for i in range(old_array.length()):

            # iterates through each node, and "puts" it into the hash table( via rehashing)
            for node in old_array[i]:
                self.put(node.key, node.value)



    def get(self, key: str) -> object:
        """
        If the hash table contains the given key, returns the value associated with that key.

        If the table does not contain the key, returns None
        """

        # hashing index for search
        index = self._hash_function(key) % self._capacity

        # need to check the entire linked list for the key (return if found)
        for node in self._buckets[index]:
            if node.key == key:
                return node.value

        # if we get to the end of the linked list, it doesn't contain the key
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns a Boolean value:

        True if the given key is contained in the hash map. False if it is not found.
        """

        # if the hash map is empty, it does not contain the key
        if self._size == 0:
            return False

        # hashing index to search for the key
        index = self._hash_function(key) % self._capacity

        # if the linked list contains the desired node, return true. False if not.
        if self._buckets[index].contains(key):
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes the key/value pair associated with the given key from the hash table if it is found.
        """

        # hashing index to search for key
        index = self._hash_function(key) % self._capacity

        # uses the given linked list remove function to remove the desired node
        if self._buckets[index].remove(key):
            self._size = self._size - 1


    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array containing every key/value pair stored in the hash map.
        """

        # initializes array for appending and output
        outputArr = DynamicArray()

        # iterates through every node in every bucket, and appends a tuple to the output
        for idx in range(self._buckets.length()):
            for node in self._buckets[idx]:
                outputArr.append((node.key, node.value))

        # returns the output after every node is iterated through
        return outputArr


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Receives: a dynamic array, sorted or not, and finds the most occurring objects in that array, and
              the frequency of their occurrence.

    Returns: Tuple containing a dynamic array of all most-occurring objects, and their frequency.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()

    # populating the hash map with frequency of occurrence
    for i in range(da.length()):
        value = 1
        # if the element has already been hashed - we need to increment the saved frequency (else, use 1)
        if map.contains_key(da[i]):
            value = map.get(da[i]) + 1
        map.put(da[i], value)

    # initialize output array and elements for tracking highest frequency
    outputModes = DynamicArray()
    currentModeFreq = 0
    maxModeFreq = 0

    # checks every object's frequency against the saved max-frequency to find all the modes
    for i in range(da.length()):
        # outputs the frequency of occurrence of the given element
        currentModeFreq = map.get(da[i])

        # if the current element's freq > saved-max, re-initialize a new array for output and append
        if currentModeFreq > maxModeFreq:
            outputModes = DynamicArray()
            outputModes.append(da[i])

            # set the value to 0 in the hash map, so we don't re-append the same values to output
            map.put(da[i], 0)
            maxModeFreq = currentModeFreq

        # if current freq = max freq, we want to add the value to the output
        elif currentModeFreq == maxModeFreq:
            outputModes.append(da[i])
            map.put(da[i], 0)

    # return tuple containing array of mode values, as well as the frequency of their occurenc
    return (outputModes, maxModeFreq)





# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(1)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
