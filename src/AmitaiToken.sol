// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "@openzeppelin-contracts-5.0.2/token/ERC20/ERC20.sol";

contract AmitaiToken is ERC20 {
    constructor() ERC20("AmitaiToken", "AMR") {
        _mint(msg.sender, 1000000 * (10 ** uint256(decimals())));
    }
}
