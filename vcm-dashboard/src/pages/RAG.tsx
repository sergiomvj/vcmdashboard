import React, { useState, useEffect } from 'react';
import { Upload, Search, Plus, Folder, FileText, Clock, CheckCircle, XCircle, AlertCircle, Download, Eye, Trash2, RefreshCw } from 'lucide-react';

interface RAGCollection {
  id: string;
  name: string;
  description: string;
  documentCount: number;
  createdAt: string;
  updatedAt: string;
  status: 'active' | 'processing' | 'error';
}

interface RAGDocument {
  id: string;
  name: string;
  type: string;
  size: number;
  collectionId: string;
  status: 'uploaded' | 'processing' | 'processed' | 'error';
  chunks: number;
  createdAt: string;
  processedAt?: string;
}

interface SearchResult {
  id: string;
  content: string;
  score: number;
  documentName: string;
  collectionName: string;
}

const RAG: React.FC = () => {
  const [collections, setCollections] = useState<RAGCollection[]>([]);
  const [documents, setDocuments] = useState<RAGDocument[]>([]);
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [selectedCollection, setSelectedCollection] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [isCollectionModalOpen, setIsCollectionModalOpen] = useState(false);
  const [isSearchModalOpen, setIsSearchModalOpen] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isProcessing, setIsProcessing] = useState(false);

  // Estados para formulários
  const [newCollectionName, setNewCollectionName] = useState('');
  const [newCollectionDescription, setNewCollectionDescription] = useState('');
  const [uploadFiles, setUploadFiles] = useState<File[]>([]);

  // Carregar dados iniciais
  useEffect(() => {
    loadCollections();
    loadDocuments();
  }, []);

  const loadCollections = async () => {
    try {
      // Simular chamada API - substituir com chamada real
      const mockCollections: RAGCollection[] = [
        {
          id: '1',
          name: 'Documentos Empresariais',
          description: 'Contratos, relatórios e documentos corporativos',
          documentCount: 12,
          createdAt: '2024-01-15',
          updatedAt: '2024-01-20',
          status: 'active'
        },
        {
          id: '2',
          name: 'Base de Conhecimento',
          description: 'Artigos, tutoriais e documentação técnica',
          documentCount: 8,
          createdAt: '2024-01-10',
          updatedAt: '2024-01-18',
          status: 'active'
        }
      ];
      setCollections(mockCollections);
    } catch (error) {
      console.error('Erro ao carregar coleções:', error);
    }
  };

  const loadDocuments = async () => {
    try {
      // Simular chamada API - substituir com chamada real
      const mockDocuments: RAGDocument[] = [
        {
          id: '1',
          name: 'Contrato_Serviços_2024.pdf',
          type: 'application/pdf',
          size: 2048576,
          collectionId: '1',
          status: 'processed',
          chunks: 45,
          createdAt: '2024-01-20',
          processedAt: '2024-01-20'
        },
        {
          id: '2',
          name: 'Relatorio_Mensal_Janeiro.docx',
          type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
          size: 1024000,
          collectionId: '1',
          status: 'processing',
          chunks: 0,
          createdAt: '2024-01-21'
        }
      ];
      setDocuments(mockDocuments);
    } catch (error) {
      console.error('Erro ao carregar documentos:', error);
    }
  };

  const handleCreateCollection = async () => {
    if (!newCollectionName.trim()) return;

    try {
      const newCollection: RAGCollection = {
        id: Date.now().toString(),
        name: newCollectionName,
        description: newCollectionDescription,
        documentCount: 0,
        createdAt: new Date().toISOString().split('T')[0],
        updatedAt: new Date().toISOString().split('T')[0],
        status: 'active'
      };

      setCollections([...collections, newCollection]);
      setNewCollectionName('');
      setNewCollectionDescription('');
      setIsCollectionModalOpen(false);
    } catch (error) {
      console.error('Erro ao criar coleção:', error);
    }
  };

  const handleFileUpload = async () => {
    if (uploadFiles.length === 0 || !selectedCollection) return;

    setIsProcessing(true);
    setUploadProgress(0);

    try {
      // Simular upload progressivo
      for (let i = 0; i <= 100; i += 10) {
        setUploadProgress(i);
        await new Promise(resolve => setTimeout(resolve, 200));
      }

      // Processar arquivos
      const newDocuments: RAGDocument[] = uploadFiles.map(file => ({
        id: Date.now().toString() + Math.random(),
        name: file.name,
        type: file.type,
        size: file.size,
        collectionId: selectedCollection,
        status: 'processing',
        chunks: 0,
        createdAt: new Date().toISOString().split('T')[0]
      }));

      setDocuments([...documents, ...newDocuments]);
      setUploadFiles([]);
      setIsUploadModalOpen(false);
      setIsProcessing(false);
      setUploadProgress(0);

      // Simular processamento
      setTimeout(() => {
        setDocuments(prev => prev.map(doc => 
          newDocuments.find(nd => nd.id === doc.id) 
            ? { ...doc, status: 'processed', chunks: Math.floor(Math.random() * 50) + 10 }
            : doc
        ));
      }, 3000);

    } catch (error) {
      console.error('Erro ao fazer upload:', error);
      setIsProcessing(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;

    try {
      // Simular busca semântica
      const mockResults: SearchResult[] = [
        {
          id: '1',
          content: 'Este documento contém informações sobre contratos de serviços empresariais...',
          score: 0.95,
          documentName: 'Contrato_Serviços_2024.pdf',
          collectionName: 'Documentos Empresariais'
        },
        {
          id: '2',
          content: 'Relatório mensal com análise de desempenho e métricas de sucesso...',
          score: 0.87,
          documentName: 'Relatorio_Mensal_Janeiro.docx',
          collectionName: 'Documentos Empresariais'
        }
      ];
      setSearchResults(mockResults);
    } catch (error) {
      console.error('Erro na busca:', error);
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'processed':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'processing':
        return <RefreshCw className="w-4 h-4 text-blue-500 animate-spin" />;
      case 'error':
        return <XCircle className="w-4 h-4 text-red-500" />;
      default:
        return <AlertCircle className="w-4 h-4 text-gray-500" />;
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Sistema RAG</h1>
          <p className="text-gray-600 mt-1">Gerenciamento de documentos e busca semântica</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => setIsSearchModalOpen(true)}
            className="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <Search className="w-4 h-4 mr-2" />
            Buscar Documentos
          </button>
          <button
            onClick={() => setIsCollectionModalOpen(true)}
            className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus className="w-4 h-4 mr-2" />
            Nova Coleção
          </button>
          <button
            onClick={() => setIsUploadModalOpen(true)}
            className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-lg hover:bg-green-700 transition-colors"
          >
            <Upload className="w-4 h-4 mr-2" />
            Upload Documento
          </button>
        </div>
      </div>

      {/* Estatísticas */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <Folder className="w-8 h-8 text-blue-500" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Coleções</p>
              <p className="text-2xl font-bold text-gray-900">{collections.length}</p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <FileText className="w-8 h-8 text-green-500" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Documentos</p>
              <p className="text-2xl font-bold text-gray-900">{documents.length}</p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <CheckCircle className="w-8 h-8 text-green-500" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Processados</p>
              <p className="text-2xl font-bold text-gray-900">
                {documents.filter(d => d.status === 'processed').length}
              </p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <Clock className="w-8 h-8 text-yellow-500" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Processando</p>
              <p className="text-2xl font-bold text-gray-900">
                {documents.filter(d => d.status === 'processing').length}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Coleções RAG */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Coleções RAG</h3>
          </div>
          <div className="p-6">
            {collections.length === 0 ? (
              <div className="text-center py-8">
                <Folder className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500">Nenhuma coleção criada ainda</p>
                <button
                  onClick={() => setIsCollectionModalOpen(true)}
                  className="mt-4 text-blue-600 hover:text-blue-700 text-sm font-medium"
                >
                  Criar primeira coleção
                </button>
              </div>
            ) : (
              <div className="space-y-4">
                {collections.map(collection => (
                  <div key={collection.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-start">
                      <div>
                        <h4 className="font-medium text-gray-900">{collection.name}</h4>
                        <p className="text-sm text-gray-600 mt-1">{collection.description}</p>
                        <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                          <span>{collection.documentCount} documentos</span>
                          <span>•</span>
                          <span>Atualizado: {collection.updatedAt}</span>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        {getStatusIcon(collection.status)}
                        <button className="text-red-600 hover:text-red-700">
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Documentos Recentes */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Documentos Recentes</h3>
          </div>
          <div className="p-6">
            {documents.length === 0 ? (
              <div className="text-center py-8">
                <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500">Nenhum documento processado</p>
                <button
                  onClick={() => setIsUploadModalOpen(true)}
                  className="mt-4 text-green-600 hover:text-green-700 text-sm font-medium"
                >
                  Fazer primeiro upload
                </button>
              </div>
            ) : (
              <div className="space-y-3">
                {documents.slice(0, 5).map(document => (
                  <div key={document.id} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
                    <div className="flex items-center gap-3">
                      {getStatusIcon(document.status)}
                      <div>
                        <p className="font-medium text-gray-900 text-sm">{document.name}</p>
                        <p className="text-xs text-gray-500">
                          {formatFileSize(document.size)} • {document.chunks} chunks
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <button className="text-gray-400 hover:text-gray-600">
                        <Eye className="w-4 h-4" />
                      </button>
                      <button className="text-gray-400 hover:text-gray-600">
                        <Download className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Modal de Upload */}
      {isUploadModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Upload de Documentos</h3>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">Coleção</label>
              <select
                value={selectedCollection || ''}
                onChange={(e) => setSelectedCollection(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Selecione uma coleção</option>
                {collections.map(collection => (
                  <option key={collection.id} value={collection.id}>
                    {collection.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">Arquivos</label>
              <input
                type="file"
                multiple
                onChange={(e) => setUploadFiles(Array.from(e.target.files || []))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              {uploadFiles.length > 0 && (
                <p className="text-sm text-gray-600 mt-2">
                  {uploadFiles.length} arquivo(s) selecionado(s)
                </p>
              )}
            </div>

            {isProcessing && (
              <div className="mb-4">
                <div className="bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${uploadProgress}%` }}
                  ></div>
                </div>
                <p className="text-sm text-gray-600 mt-2">Processando... {uploadProgress}%</p>
              </div>
            )}

            <div className="flex justify-end gap-3">
              <button
                onClick={() => {
                  setIsUploadModalOpen(false);
                  setUploadFiles([]);
                  setUploadProgress(0);
                  setIsProcessing(false);
                }}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
              >
                Cancelar
              </button>
              <button
                onClick={handleFileUpload}
                disabled={!selectedCollection || uploadFiles.length === 0 || isProcessing}
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                Fazer Upload
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal de Nova Coleção */}
      {isCollectionModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Nova Coleção RAG</h3>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">Nome</label>
              <input
                type="text"
                value={newCollectionName}
                onChange={(e) => setNewCollectionName(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Ex: Documentos Empresariais"
              />
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">Descrição</label>
              <textarea
                value={newCollectionDescription}
                onChange={(e) => setNewCollectionDescription(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows={3}
                placeholder="Descrição da coleção..."
              />
            </div>

            <div className="flex justify-end gap-3">
              <button
                onClick={() => {
                  setIsCollectionModalOpen(false);
                  setNewCollectionName('');
                  setNewCollectionDescription('');
                }}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
              >
                Cancelar
              </button>
              <button
                onClick={handleCreateCollection}
                disabled={!newCollectionName.trim()}
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                Criar Coleção
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal de Busca */}
      {isSearchModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[80vh] overflow-hidden flex flex-col">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Busca Semântica</h3>
            
            <div className="mb-4">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="O que você está procurando?"
                />
                <button
                  onClick={handleSearch}
                  className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700"
                >
                  <Search className="w-4 h-4" />
                </button>
              </div>
            </div>

            <div className="flex-1 overflow-y-auto">
              {searchResults.length === 0 ? (
                <div className="text-center py-8">
                  <Search className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">Faça uma busca para encontrar documentos relevantes</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {searchResults.map(result => (
                    <div key={result.id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <h4 className="font-medium text-gray-900">{result.documentName}</h4>
                          <p className="text-sm text-gray-600">{result.collectionName}</p>
                        </div>
                        <span className="text-sm font-medium text-blue-600">
                          {(result.score * 100).toFixed(0)}% match
                        </span>
                      </div>
                      <p className="text-sm text-gray-700">{result.content}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="flex justify-end mt-4">
              <button
                onClick={() => {
                  setIsSearchModalOpen(false);
                  setSearchQuery('');
                  setSearchResults([]);
                }}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
              >
                Fechar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RAG;