// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LoopStorage {
    uint256[] public values;

    function storeValues(uint256 n) public {
        for (uint256 i = 0; i < n; i++) {
            values.push(i);
        }
    }

    function getValues() public view returns (uint256[] memory) {
        return values;
    }
}
