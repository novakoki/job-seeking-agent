'use client';

import * as React from 'react';

import Box from '@mui/material/Box';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Link } from '@mui/material';

interface Job {
  id: string;
  role: string;
  company: string;
  location: string;
  link: string;
  date: string;
}

export default function DataGridDemo() {
  const [data, setData] = React.useState<Job[]>([]);
  React.useEffect(() => {
    fetch('/api/jobs')
      .then((res) => res.json())
      .then((data) => setData(data));
  }, []);

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 90 },
    { field: 'role', headerName: 'Role', width: 150 },
    { field: 'company', headerName: 'Company', width: 150 },
    { field: 'location', headerName: 'Location', width: 150 },
    { field: 'link', headerName: 'Link', width: 150, renderCell: (params) => <Link href={params.value} target="_blank" rel="noopener">{params.value}</Link> },
    { field: 'date', headerName: 'Date', width: 150, type: "date", valueGetter: (v, r, c) => new Date(v) },
    { field: 'source', headerName: 'Source', width: 150 },
  ];

  return (
    <Box sx={{ width: '100%' }}>
      <DataGrid
        rows={data}
        columns={columns}
        initialState={{
          pagination: {
            paginationModel: {
              pageSize: 100,
            },
          },
        }}
        pageSizeOptions={[100]}
        checkboxSelection
        disableRowSelectionOnClick
      />
    </Box>
  );
}



