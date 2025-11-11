import { NextRequest, NextResponse } from 'next/server';

export async function GET(
  request: NextRequest,
  { params }: { params: { empresa_id: string } }
) {
  try {
    const { empresa_id } = params;
    
    // Mock RAG status
    const mockStatus = {
      empresa_id,
      rag_status: 'active',
      total_documents: 150,
      total_embeddings: 300,
      last_updated: new Date().toISOString(),
      database_status: 'connected',
      ingestion_status: 'completed'
    };

    return NextResponse.json(mockStatus);

  } catch (error) {
    console.error('Erro ao buscar status RAG:', error);
    return NextResponse.json(
      { error: 'Erro interno do servidor' },
      { status: 500 }
    );
  }
}