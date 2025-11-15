"""
Modelos de dados para o PluginForge Studio
Sistema de usuários, plugins e chat
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, UTC
import uuid

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Modelo de usuário com autenticação"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    
    # Subscription information
    subscription_plan = db.Column(db.String(20), default='basic')  # basic, pro, premium
    subscription_status = db.Column(db.String(20), default='active')  # active, cancelled, expired
    subscription_start = db.Column(db.DateTime)
    subscription_end = db.Column(db.DateTime)
    
    # Relacionamentos
    plugins = db.relationship('Plugin', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash da senha"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verificar senha"""
        return check_password_hash(self.password_hash, password)
    
    def get_plan_display(self):
        """Get formatted plan name for display"""
        plan_names = {
            'basic': 'FREE PLAN',
            'pro': 'PRO PLAN',
            'premium': 'PREMIUM PLAN'
        }
        return plan_names.get(self.subscription_plan, 'FREE PLAN')
    
    def __repr__(self):
        return f'<User {self.username}>'

class Plugin(db.Model):
    """Modelo de plugin com histórico e status"""
    __tablename__ = 'plugins'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Informações básicas do plugin
    name = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(20), default='1.0.0')
    minecraft_version = db.Column(db.String(20), default='1.20.1')
    description = db.Column(db.Text)
    plugin_author = db.Column(db.String(100))
    features = db.Column(db.Text)
    
    # Status do plugin
    status = db.Column(db.String(20), default='draft')  # draft, generating, compiled, error
    compiled_file = db.Column(db.String(255))  # Caminho para o arquivo compilado
    last_compile_attempt = db.Column(db.DateTime)
    error_message = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    
    # Relacionamentos
    chats = db.relationship('Chat', backref='plugin', lazy=True, cascade='all, delete-orphan')
    versions = db.relationship('PluginVersion', backref='plugin', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Plugin {self.name}>'

class Chat(db.Model):
    """Modelo de chat para cada plugin"""
    __tablename__ = 'chats'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    plugin_id = db.Column(db.String(36), db.ForeignKey('plugins.id'), nullable=False)
    
    # Informações do chat
    title = db.Column(db.String(200), default='Nova Conversa')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    
    # Relacionamentos
    messages = db.relationship('Message', backref='chat', lazy=True, cascade='all, delete-orphan', order_by='Message.created_at')
    
    def __repr__(self):
        return f'<Chat {self.title}>'

class Message(db.Model):
    """Modelo de mensagem no chat"""
    __tablename__ = 'messages'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    chat_id = db.Column(db.String(36), db.ForeignKey('chats.id'), nullable=False)
    
    # Tipo e conteúdo da mensagem
    role = db.Column(db.String(20), nullable=False)  # user, assistant, system
    content = db.Column(db.Text, nullable=False)
    content_type = db.Column(db.String(20), default='text')  # text, code, plugin_update
    
    # Dados da geração (para assistant)
    generated_code = db.Column(db.Text)  # Código Java gerado
    plugin_yml = db.Column(db.Text)      # plugin.yml gerado
    package_name = db.Column(db.String(100))  # Nome do pacote
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    
    def __repr__(self):
        return f'<Message {self.role}: {self.content[:50]}>'

class PluginVersion(db.Model):
    """Histórico de versões do plugin"""
    __tablename__ = 'plugin_versions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    plugin_id = db.Column(db.String(36), db.ForeignKey('plugins.id'), nullable=False)
    
    # Informações da versão
    version_number = db.Column(db.String(20), nullable=False)
    changes = db.Column(db.Text)  # Descrição das mudanças
    
    # Código da versão
    main_code = db.Column(db.Text)
    plugin_yml_content = db.Column(db.Text)
    package_name = db.Column(db.String(100))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    
    def __repr__(self):
        return f'<PluginVersion {self.plugin.name} v{self.version_number}>'

def init_db(app):
    """Inicializar banco de dados"""
    db.init_app(app)
    
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        
        # Verificar se já existe um usuário admin
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(username='admin', email='admin@pluginforge.com')
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Usuário admin criado: admin / admin123")