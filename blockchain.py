import hashlib
import json
from datetime import datetime
from models import BlockchainBlock
from app import db

class SimpleBlockchain:
    """
    A simple blockchain implementation for certificate hash storage
    """
    
    def __init__(self):
        self.difficulty = 2  # Number of leading zeros required for valid hash
    
    def get_latest_block(self):
        """Get the latest block in the blockchain"""
        return BlockchainBlock.query.order_by(BlockchainBlock.id.desc()).first()
    
    def create_genesis_block(self):
        """Create the genesis block if it doesn't exist"""
        if BlockchainBlock.query.count() == 0:
            genesis_block = BlockchainBlock(
                block_hash="0" * 64,
                previous_hash="0" * 64,
                certificate_hash="genesis",
                nonce=0
            )
            db.session.add(genesis_block)
            db.session.commit()
            return genesis_block
        return self.get_latest_block()
    
    def calculate_hash(self, previous_hash, certificate_hash, timestamp, nonce):
        """Calculate hash for a block"""
        data = {
            'previous_hash': previous_hash,
            'certificate_hash': certificate_hash,
            'timestamp': timestamp.isoformat(),
            'nonce': nonce
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
    
    def mine_block(self, certificate_hash):
        """
        Mine a new block with the certificate hash
        Uses proof-of-work algorithm
        """
        # Ensure genesis block exists
        latest_block = self.get_latest_block()
        if not latest_block:
            latest_block = self.create_genesis_block()
        
        previous_hash = latest_block.block_hash
        timestamp = datetime.utcnow()
        nonce = 0
        
        # Mine the block (find a hash with required difficulty)
        while True:
            block_hash = self.calculate_hash(previous_hash, certificate_hash, timestamp, nonce)
            
            # Check if hash meets difficulty requirement
            if block_hash.startswith("0" * self.difficulty):
                break
            
            nonce += 1
        
        # Create and save the new block
        new_block = BlockchainBlock(
            block_hash=block_hash,
            previous_hash=previous_hash,
            certificate_hash=certificate_hash,
            timestamp=timestamp,
            nonce=nonce
        )
        
        db.session.add(new_block)
        db.session.commit()
        
        return new_block
    
    def verify_blockchain_integrity(self):
        """Verify the integrity of the entire blockchain"""
        blocks = BlockchainBlock.query.order_by(BlockchainBlock.id.asc()).all()
        
        if not blocks:
            return True
        
        # Check each block
        for i in range(len(blocks)):
            current_block = blocks[i]
            
            # Verify block hash
            calculated_hash = self.calculate_hash(
                current_block.previous_hash,
                current_block.certificate_hash,
                current_block.timestamp,
                current_block.nonce
            )
            
            if calculated_hash != current_block.block_hash:
                return False
            
            # Verify link to previous block
            if i > 0:
                previous_block = blocks[i-1]
                if current_block.previous_hash != previous_block.block_hash:
                    return False
        
        return True
    
    def get_certificate_verification(self, certificate_hash):
        """Verify if a certificate hash exists in the blockchain"""
        block = BlockchainBlock.query.filter_by(certificate_hash=certificate_hash).first()
        
        if block:
            return {
                'verified': True,
                'block_id': block.id,
                'block_hash': block.block_hash,
                'timestamp': block.timestamp,
                'nonce': block.nonce
            }
        
        return {'verified': False}
    
    def get_blockchain_stats(self):
        """Get blockchain statistics"""
        total_blocks = BlockchainBlock.query.count()
        latest_block = self.get_latest_block()
        
        return {
            'total_blocks': total_blocks,
            'latest_block_hash': latest_block.block_hash[:16] + '...' if latest_block else None,
            'latest_timestamp': latest_block.timestamp if latest_block else None,
            'integrity_valid': self.verify_blockchain_integrity()
        }

# Global blockchain instance
blockchain = SimpleBlockchain()
