pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract BusinessRegistry is ERC721Full {
    constructor() public ERC721Full("BusinessRegistryToken", "BRT") {}

    struct Business {
        string businessName;
        string ownerName;
        uint256 phoneNumber;
    }

    mapping(uint256 => Business) public businessListing;

    event editRegistry(uint256 tokenId, uint256 phoneNumber, string reportURI);

    function registerBusiness(
        address owner,
        string memory businessName,
        string memory ownerName,
        uint256 initialPhoneNumber,
        string memory tokenURI
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();

        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);

        businessListing[tokenId] = Business(businessName, ownerName, initialPhoneNumber);

        return tokenId;
    }

    function editPhoneNumber(
        uint256 tokenId,
        uint256 newPhoneNumber,
        string memory reportURI
    ) public returns (uint256) {
        businessListing[tokenId].phoneNumber = newPhoneNumber;

        emit editRegistry(tokenId, newPhoneNumber, reportURI);

        return businessListing[tokenId].phoneNumber;
    }
}
