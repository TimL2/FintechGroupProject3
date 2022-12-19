pragma solidity ^0.6.0;

contract MyContract {
    // The address of the wallet that holds the token
    address private tokenHolder;

    // The function that can only be called by the token holder
    function protectedFunction() public {
        // Check if the caller is the token holder
        require(msg.sender == tokenHolder, "Only the token holder can call this function");

        // Function code goes here
    }
}
