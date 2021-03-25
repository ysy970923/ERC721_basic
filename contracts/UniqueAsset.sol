// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract UniqueAsset is ERC721 {
    using Counters for Counters.Counter;

    Counters.Counter private _tokenIds;
    mapping(string => bool) hashMade;
    mapping(uint256 => uint256) tokenPrice;
    mapping(uint256 => string) tokenHash;

    constructor() ERC721("UniqueAsset", "UNA") {}

    function createToken(string memory hash, uint256 price)
        public
        returns (uint256)
    {
        require(hashMade[hash] == false);
        hashMade[hash] = true;
        _tokenIds.increment();
        uint256 newTokenId = _tokenIds.current();
        _mint(msg.sender, newTokenId);

        tokenPrice[newTokenId] = price;
        return newTokenId;
    }

    function buyToken(uint256 tokenId) public payable {
        getApproved(tokenId);

        uint256 _bidAmount = msg.value;
        uint256 price = tokenPrice[tokenId];

        require(_bidAmount >= price, 'error here');
        address payable seller = payable(ownerOf(tokenId));
        
        seller.transfer(price);
        payable(msg.sender).transfer(_bidAmount-price);
        
        _transfer(seller, msg.sender, tokenId);
    }
}
