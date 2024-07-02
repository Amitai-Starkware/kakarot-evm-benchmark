// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract ComplexContract {
    uint256 public counter;
    mapping(uint256 => uint256) public values;
    event ValueAdded(uint256 indexed key, uint256 value);

    function incrementCounter() public {
        counter++;
    }

    function addValue(uint256 key, uint256 value) public {
        values[key] = value;
        emit ValueAdded(key, value);
    }

    function computeFactorial(uint256 n) public pure returns (uint256) {
        if (n == 0) {
            return 1;
        } else {
            return n * computeFactorial(n - 1);
        }
    }

    function findMax(uint256[] memory arr) public pure returns (uint256) {
        require(arr.length > 0, "Array is empty");
        uint256 max = arr[0];
        for (uint256 i = 1; i < arr.length; i++) {
            if (arr[i] > max) {
                max = arr[i];
            }
        }
        return max;
    }

    function calculateSum(uint256[] memory arr) public pure returns (uint256) {
        uint256 sum = 0;
        for (uint256 i = 0; i < arr.length; i++) {
            sum += arr[i];
        }
        return sum;
    }
}
